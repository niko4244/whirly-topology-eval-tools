import React, { useEffect, useState } from "react";
import { fetchComponents, deleteComponent } from "../api/components";

export default function ComponentList() {
  const [components, setComponents] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const res = await fetchComponents(query);
      setComponents(res.data);
    } catch (err) {
      setError("Error loading components");
    }
  }

  useEffect(() => { load(); }, [query]);

  async function handleDelete(id) {
    try {
      await deleteComponent(id);
      load();
    } catch {
      setError("Delete failed");
    }
  }

  return (
    <div>
      <input placeholder="Search components" value={query} onChange={e => setQuery(e.target.value)} />
      {error && <div>{error}</div>}
      <ul>
        {components.map(comp => (
          <li key={comp.id}>
            {comp.name} ({comp.type})
            <button onClick={() => handleDelete(comp.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}