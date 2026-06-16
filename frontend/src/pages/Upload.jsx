import React, { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { uploadCsv } from "../api/client.js";

export default function Upload({ onAnalysisReady }) {
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFiles = useCallback(
    async (fileList) => {
      const files = Array.from(fileList).filter((f) => f.name.toLowerCase().endsWith(".csv"));
      if (files.length === 0) {
        setError("Merci de sélectionner au moins un fichier CSV.");
        return;
      }
      setError(null);
      setLoading(true);
      try {
        const result = await uploadCsv(files);
        onAnalysisReady(result);
        navigate("/dashboard");
      } catch (e) {
        setError(e?.response?.data?.detail || "Erreur lors de l'analyse du fichier.");
      } finally {
        setLoading(false);
      }
    },
    [navigate, onAnalysisReady]
  );

  return (
    <div>
      <h2>Importer des fichiers CSV</h2>
      <p>Glissez-déposez un ou plusieurs fichiers CSV (jusqu'à 100 000 lignes chacun).</p>
      <div
        className={`dropzone ${dragOver ? "dragover" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => document.getElementById("file-input").click()}
      >
        {loading ? "Analyse en cours…" : "Cliquez ou déposez vos fichiers CSV ici"}
        <input
          id="file-input"
          type="file"
          accept=".csv"
          multiple
          style={{ display: "none" }}
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>
      {error && <p style={{ color: "#b91c1c" }}>{error}</p>}
    </div>
  );
}
