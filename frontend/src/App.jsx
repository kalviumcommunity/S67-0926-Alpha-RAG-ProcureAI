import { useCallback, useEffect, useRef, useState } from "react";
import { api, streamChat } from "./api.js";

const DOC_TYPES = ["contract", "pricing_agreement", "compliance_document", "other"];
const STATUSES = ["uploaded", "processing", "processed", "failed"];
const label = (s) => s.replace(/_/g, " ");

function useLoad(fn, deps = []) {
  const [data, setData] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const reload = useCallback(async () => {
    setLoading(true);
    try { setData(await fn()); setError(""); }
    catch (e) { setError(e.message); }
    finally { setLoading(false); }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  useEffect(() => { reload(); }, [reload]);
  return { data, error, loading, reload };
}

const Error_ = ({ msg }) => (msg ? <div className="alert">{msg}</div> : null);

/* ---------------- Suppliers ---------------- */
function Suppliers() {
  const { data, error, loading, reload } = useLoad(api.listSuppliers);
  const [form, setForm] = useState({ name: "", contact_information: "" });
  const [editing, setEditing] = useState(null);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      if (editing) await api.updateSupplier(editing, form);
      else await api.createSupplier(form);
      setForm({ name: "", contact_information: "" });
      setEditing(null); setErr(""); reload();
    } catch (e2) { setErr(e2.message); }
  };
  const remove = async (s) => {
    if (!confirm(`Delete supplier "${s.name}"?`)) return;
    try { await api.deleteSupplier(s.id); reload(); } catch (e2) { setErr(e2.message); }
  };

  return (
    <section>
      <h2>Suppliers</h2>
      <form className="card row" onSubmit={submit}>
        <input required placeholder="Supplier name" value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input placeholder="Contact information" value={form.contact_information}
          onChange={(e) => setForm({ ...form, contact_information: e.target.value })} />
        <button className="primary">{editing ? "Save" : "Add supplier"}</button>
        {editing && <button type="button" onClick={() => { setEditing(null); setForm({ name: "", contact_information: "" }); }}>Cancel</button>}
      </form>
      <Error_ msg={err || error} />
      <div className="card">
        {loading ? <p className="muted">Loading…</p> : data.length === 0 ? <p className="muted">No suppliers yet.</p> : (
          <table>
            <thead><tr><th>Name</th><th>Contact</th><th>Created</th><th /></tr></thead>
            <tbody>
              {data.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.contact_information || "—"}</td>
                  <td>{new Date(s.created_at).toLocaleDateString()}</td>
                  <td className="actions">
                    <button onClick={() => { setEditing(s.id); setForm({ name: s.name, contact_information: s.contact_information || "" }); }}>Edit</button>
                    <button className="danger" onClick={() => remove(s)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}

/* ---------------- Documents ---------------- */
function Documents() {
  const suppliers = useLoad(api.listSuppliers);
  const [filters, setFilters] = useState({ supplier_id: "", document_type: "", status: "" });
  const docs = useLoad(() => api.listDocuments(filters), [filters.supplier_id, filters.document_type, filters.status]);
  const [up, setUp] = useState({ supplier_id: "", document_type: "contract", file: null });
  const [busy, setBusy] = useState({});
  const [err, setErr] = useState("");
  const [meta, setMeta] = useState(null);
  const fileRef = useRef();

  const supplierName = (id) => suppliers.data.find((s) => s.id === id)?.name ?? `#${id}`;

  const upload = async (e) => {
    e.preventDefault();
    setBusy((b) => ({ ...b, upload: true }));
    try {
      await api.uploadDocument(up);
      setUp({ ...up, file: null }); fileRef.current.value = ""; setErr(""); docs.reload();
    } catch (e2) { setErr(e2.message); }
    finally { setBusy((b) => ({ ...b, upload: false })); }
  };
  const act = async (id, fn) => {
    setBusy((b) => ({ ...b, [id]: true }));
    try { await fn(); setErr(""); } catch (e2) { setErr(e2.message); }
    finally { setBusy((b) => ({ ...b, [id]: false })); docs.reload(); }
  };
  const showMeta = async (id) => {
    try { setMeta({ id, ...(await api.documentMetadata(id)) }); } catch (e2) { setMeta({ id, error: e2.message }); }
  };

  return (
    <section>
      <h2>Documents</h2>
      <form className="card row" onSubmit={upload}>
        <select required value={up.supplier_id} onChange={(e) => setUp({ ...up, supplier_id: e.target.value })}>
          <option value="">Supplier…</option>
          {suppliers.data.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <select value={up.document_type} onChange={(e) => setUp({ ...up, document_type: e.target.value })}>
          {DOC_TYPES.map((t) => <option key={t} value={t}>{label(t)}</option>)}
        </select>
        <input ref={fileRef} required type="file" accept=".pdf,.docx,.txt"
          onChange={(e) => setUp({ ...up, file: e.target.files[0] })} />
        <button className="primary" disabled={busy.upload}>{busy.upload ? "Uploading…" : "Upload"}</button>
      </form>

      <div className="row filters">
        <select value={filters.supplier_id} onChange={(e) => setFilters({ ...filters, supplier_id: e.target.value })}>
          <option value="">All suppliers</option>
          {suppliers.data.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <select value={filters.document_type} onChange={(e) => setFilters({ ...filters, document_type: e.target.value })}>
          <option value="">All types</option>
          {DOC_TYPES.map((t) => <option key={t} value={t}>{label(t)}</option>)}
        </select>
        <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
          <option value="">All statuses</option>
          {STATUSES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      <Error_ msg={err || docs.error} />
      <div className="card">
        {docs.loading ? <p className="muted">Loading…</p> : docs.data.length === 0 ? <p className="muted">No documents found.</p> : (
          <table>
            <thead><tr><th>File</th><th>Supplier</th><th>Type</th><th>Size</th><th>Status</th><th /></tr></thead>
            <tbody>
              {docs.data.map((d) => (
                <tr key={d.id}>
                  <td>{d.filename}</td>
                  <td>{supplierName(d.supplier_id)}</td>
                  <td>{label(d.document_type)}</td>
                  <td>{(d.file_size / 1024).toFixed(0)} KB</td>
                  <td><span className={`badge ${d.status}`}>{d.status}</span></td>
                  <td className="actions">
                    {(d.status === "uploaded" || d.status === "failed") && (
                      <button className="primary" disabled={busy[d.id]} onClick={() => act(d.id, () => api.processDocument(d.id))}>
                        {busy[d.id] ? "Processing…" : d.status === "failed" ? "Retry" : "Process"}
                      </button>
                    )}
                    {d.status === "processed" && <button onClick={() => showMeta(d.id)}>Metadata</button>}
                    <button className="danger" disabled={busy[d.id]} onClick={() => confirm(`Delete "${d.filename}"?`) && act(d.id, () => api.deleteDocument(d.id))}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {meta && (
        <div className="card">
          <div className="row between"><strong>Metadata — document #{meta.id}</strong><button onClick={() => setMeta(null)}>Close</button></div>
          {meta.error ? <p className="muted">{meta.error}</p> : (
            <dl>
              {["title", "effective_date", "expiry_date", "version", "language"].map((k) => (
                <div key={k}><dt>{label(k)}</dt><dd>{meta[k] || "—"}</dd></div>
              ))}
            </dl>
          )}
        </div>
      )}
    </section>
  );
}

/* ---------------- Chat ---------------- */
function Chat() {
  const docs = useLoad(() => api.listDocuments({ status: "processed" }));
  const [selected, setSelected] = useState([]);
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef();
  const endRef = useRef();

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [turns]);

  const patchLast = (fn) => setTurns((t) => t.map((x, i) => (i === t.length - 1 ? fn(x) : x)));

  const ask = async (e) => {
    e.preventDefault();
    const q = question.trim();
    if (!q || streaming) return;
    setQuestion("");
    setTurns((t) => [...t, { q, a: "", sources: [], error: "" }]);
    setStreaming(true);
    abortRef.current = new AbortController();
    try {
      await streamChat(
        { question: q, document_ids: selected.length ? selected : null },
        {
          signal: abortRef.current.signal,
          onChunk: (c) => patchLast((x) => ({ ...x, a: x.a + c })),
          onSources: (s) => patchLast((x) => ({ ...x, sources: s })),
          onError: (d) => patchLast((x) => ({ ...x, error: d })),
        }
      );
    } catch (e2) {
      if (e2.name !== "AbortError") patchLast((x) => ({ ...x, error: e2.message }));
    } finally { setStreaming(false); }
  };

  const toggle = (id) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  return (
    <section className="chat">
      <h2>Ask your documents</h2>
      <div className="card">
        <div className="row between">
          <strong>Search scope</strong>
          <span className="muted">{selected.length ? `${selected.length} selected` : "All processed documents"}</span>
        </div>
        {docs.data.length === 0 ? <p className="muted">No processed documents yet. Process one in Documents first.</p> : (
          <div className="chips">
            {docs.data.map((d) => (
              <label key={d.id} className={`chip ${selected.includes(d.id) ? "on" : ""}`}>
                <input type="checkbox" checked={selected.includes(d.id)} onChange={() => toggle(d.id)} />
                {d.filename}
              </label>
            ))}
          </div>
        )}
      </div>

      <div className="thread">
        {turns.length === 0 && <p className="muted">Try: “What are the payment terms?”</p>}
        {turns.map((t, i) => (
          <div key={i} className="turn">
            <div className="q">{t.q}</div>
            <div className="a">
              {t.a || (!t.error && "Thinking…")}
              {t.error && <div className="alert">{t.error}</div>}
              {t.sources.length > 0 && (
                <details open>
                  <summary>{t.sources.length} source{t.sources.length > 1 ? "s" : ""}</summary>
                  {t.sources.map((s, j) => (
                    <blockquote key={j}>
                      <div className="src-head">{s.document_name} · page {s.page}</div>
                      {s.excerpt}
                    </blockquote>
                  ))}
                </details>
              )}
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      <form className="row ask" onSubmit={ask}>
        <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask a question about your procurement documents…" />
        {streaming
          ? <button type="button" onClick={() => abortRef.current?.abort()}>Stop</button>
          : <button className="primary" disabled={!question.trim()}>Ask</button>}
      </form>
    </section>
  );
}

/* ---------------- Shell ---------------- */
const TABS = { Chat, Documents, Suppliers };

export default function App() {
  const [tab, setTab] = useState("Chat");
  const [online, setOnline] = useState(null);
  useEffect(() => { api.health().then(() => setOnline(true), () => setOnline(false)); }, []);
  const View = TABS[tab];

  return (
    <div className="app">
      <aside>
        <h1>Procurement<br />Intelligence</h1>
        <nav>
          {Object.keys(TABS).map((t) => (
            <button key={t} className={t === tab ? "active" : ""} onClick={() => setTab(t)}>{t}</button>
          ))}
        </nav>
        <div className="status"><i className={online === null ? "" : online ? "ok" : "bad"} />{online === null ? "Checking API…" : online ? "API connected" : "API unreachable"}</div>
      </aside>
      <main><View /></main>
    </div>
  );
}
