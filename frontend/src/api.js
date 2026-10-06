const BASE = import.meta.env.VITE_API_BASE || "";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}/api${path}`, options);
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") detail = body.detail;
      else if (Array.isArray(body.detail)) detail = body.detail.map((d) => d.msg).join("; ");
    } catch {}
    throw new Error(detail);
  }
  return res.json();
}

const json = (method, body) => ({
  method,
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

export const api = {
  listSuppliers: () => request("/suppliers"),
  createSupplier: (b) => request("/suppliers", json("POST", b)),
  updateSupplier: (id, b) => request(`/suppliers/${id}`, json("PUT", b)),
  deleteSupplier: (id) => request(`/suppliers/${id}`, { method: "DELETE" }),

  listDocuments: (filters = {}) => {
    const q = new URLSearchParams(Object.entries(filters).filter(([, v]) => v)).toString();
    return request(`/documents${q ? `?${q}` : ""}`);
  },
  uploadDocument: ({ file, supplier_id, document_type }) => {
    const fd = new FormData();
    fd.append("file", file);
    fd.append("supplier_id", supplier_id);
    fd.append("document_type", document_type);
    return request("/documents/upload", { method: "POST", body: fd });
  },
  processDocument: (id) => request(`/documents/${id}/process`, { method: "POST" }),
  deleteDocument: (id) => request(`/documents/${id}`, { method: "DELETE" }),
  documentMetadata: (id) => request(`/documents/${id}/metadata`),

  health: () => request("/health"),
  chat: (b) => request("/chat", json("POST", b)),
};

// Streams /api/chat/stream (SSE over POST). Callbacks: onChunk, onSources, onError.
export async function streamChat(body, { onChunk, onSources, onError, signal }) {
  const res = await fetch(`${BASE}/api/chat/stream`, {
    ...json("POST", body),
    signal,
  });
  if (!res.ok || !res.body) throw new Error(`Stream failed (${res.status})`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  const dispatch = (raw) => {
    let event = "message";
    let data = "";
    for (const line of raw.split("\n")) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) data += line.slice(5).trim();
    }
    if (!data) return;
    const payload = JSON.parse(data);
    if (event === "chunk") onChunk(payload.content);
    else if (event === "sources") onSources(payload.sources);
    else if (event === "error") onError(payload.detail);
  };

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
    let i;
    while ((i = buffer.indexOf("\n\n")) !== -1) {
      dispatch(buffer.slice(0, i));
      buffer = buffer.slice(i + 2);
    }
  }
}
