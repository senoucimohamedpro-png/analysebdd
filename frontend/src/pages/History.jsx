import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHistory, getSummary } from "../api/client.js";

export default function History({ onSelect }) {
  const [entries, setEntries] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    getHistory().then(setEntries).catch(() => setError("Impossible de charger l'historique."));
  }, []);

  const openAnalysis = async (analysisId) => {
    try {
      const summary = await getSummary(analysisId);
      onSelect(summary);
      navigate("/dashboard");
    } catch {
      setError("Cette analyse n'est plus disponible en cache (relancez l'analyse depuis le fichier d'origine).");
    }
  };

  return (
    <div>
      <h2>Historique des analyses</h2>
      {error && <p style={{ color: "#b91c1c" }}>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Fichier(s)</th>
            <th>Durée</th>
            <th>Total fiches</th>
            <th>Actives</th>
            <th>Bloquées</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e) => (
            <tr key={e.analysis_id}>
              <td>{new Date(e.date_analyse).toLocaleString("fr-FR")}</td>
              <td>{e.nom_fichier}</td>
              <td>{e.duree_secondes}s</td>
              <td>{e.total_fiches.toLocaleString("fr-FR")}</td>
              <td>{e.fiches_actives.toLocaleString("fr-FR")}</td>
              <td>{e.fiches_bloquees.toLocaleString("fr-FR")}</td>
              <td><button className="primary" onClick={() => openAnalysis(e.analysis_id)}>Ouvrir</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      {entries.length === 0 && <p>Aucune analyse enregistrée pour le moment.</p>}
    </div>
  );
}
