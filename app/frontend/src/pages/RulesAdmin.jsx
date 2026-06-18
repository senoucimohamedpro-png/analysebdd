import React, { useEffect, useState } from "react";
import {
  getBlockingRules, updateBlockingRules,
  getClassificationRules, updateClassificationRules,
} from "../api/client.js";

function JsonEditor({ title, description, loader, saver }) {
  const [text, setText] = useState("");
  const [status, setStatus] = useState(null);

  useEffect(() => {
    loader().then((data) => setText(JSON.stringify(data, null, 2)));
  }, []);

  const save = async () => {
    try {
      const parsed = JSON.parse(text);
      await saver(parsed);
      setStatus({ ok: true, msg: "Règles enregistrées." });
    } catch (e) {
      setStatus({ ok: false, msg: e?.response?.data?.detail || "JSON invalide ou erreur d'enregistrement." });
    }
  };

  return (
    <div className="card" style={{ marginBottom: 20 }}>
      <h3>{title}</h3>
      <p style={{ color: "#64748b", fontSize: 13 }}>{description}</p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={16}
        style={{ width: "100%", fontFamily: "monospace", fontSize: 13, padding: 10 }}
      />
      <div style={{ marginTop: 10 }}>
        <button className="primary" onClick={save}>Enregistrer</button>
        {status && (
          <span style={{ marginLeft: 12, color: status.ok ? "#15803d" : "#b91c1c" }}>{status.msg}</span>
        )}
      </div>
    </div>
  );
}

export default function RulesAdmin() {
  return (
    <div>
      <h2>Référentiel IT & Règles de classification</h2>
      <JsonEditor
        title="Règles de blocage (référentiel IT)"
        description="Conditions dynamiques appliquées sur les colonnes du CSV (ex: priorite) pour déterminer si une fiche est bloquée. Modifiable sans redéploiement."
        loader={getBlockingRules}
        saver={updateBlockingRules}
      />
      <JsonEditor
        title="Règles de classification (positif / traité)"
        description="Listes de valeurs de contact_qualif1 définissant les fiches positives et traitées."
        loader={getClassificationRules}
        saver={updateClassificationRules}
      />
    </div>
  );
}
