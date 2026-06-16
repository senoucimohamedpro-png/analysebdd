import React, { useEffect, useMemo, useState } from "react";
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, CartesianGrid,
} from "recharts";
import { getFiches, exportUrl } from "../api/client.js";

const COLORS = {
  "Positive": "#22c55e",
  "Traitée (autre)": "#6366f1",
  "Bloquée": "#ef4444",
  "Non traitée (active)": "#f59e0b",
};

const TAG_CLASS = {
  "Positive": "tag-positive",
  "Bloquée": "tag-blocked",
  "Traitée (autre)": "tag-other",
  "Non traitée (active)": "tag-active",
};

function KpiCards({ kpi }) {
  const items = [
    ["Total fiches", kpi.total_fiches],
    ["Traitées", kpi.fiches_traitees],
    ["Positives", kpi.fiches_positives],
    ["Non traitées", kpi.fiches_non_traitees],
    ["Bloquées", kpi.fiches_bloquees],
    ["Actives", kpi.fiches_actives],
  ];
  return (
    <div className="kpi-grid">
      {items.map(([label, value]) => (
        <div className="kpi-card" key={label}>
          <div className="label">{label}</div>
          <div className="value">{value.toLocaleString("fr-FR")}</div>
        </div>
      ))}
    </div>
  );
}

export default function Dashboard({ analysis }) {
  const [filters, setFilters] = useState({ statut: "", code_marketing: "", date_chargement: "" });
  const [fiches, setFiches] = useState([]);
  const [total, setTotal] = useState(0);
  const [sortKey, setSortKey] = useState(null);
  const [sortDir, setSortDir] = useState(1);

  useEffect(() => {
    const params = {};
    if (filters.statut) params.statut = filters.statut;
    if (filters.code_marketing) params.code_marketing = filters.code_marketing;
    if (filters.date_chargement) params.date_chargement = filters.date_chargement;
    getFiches(analysis.analysis_id, params).then((r) => {
      setFiches(r.fiches);
      setTotal(r.total);
    });
  }, [filters, analysis.analysis_id]);

  const codesMarketing = useMemo(
    () => Array.from(new Set(analysis.apercu_fiches.map((f) => f.code_marketing))).filter(Boolean),
    [analysis]
  );

  const sortedFiches = useMemo(() => {
    if (!sortKey) return fiches;
    return [...fiches].sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (av < bv) return -1 * sortDir;
      if (av > bv) return 1 * sortDir;
      return 0;
    });
  }, [fiches, sortKey, sortDir]);

  const toggleSort = (key) => {
    if (sortKey === key) setSortDir((d) => -d);
    else { setSortKey(key); setSortDir(1); }
  };

  return (
    <div>
      <h2>Dashboard — {analysis.nom_fichier}</h2>
      <p style={{ color: "#64748b" }}>
        Analysé le {new Date(analysis.date_analyse).toLocaleString("fr-FR")} en {analysis.duree_secondes}s
        &nbsp;·&nbsp; {analysis.total_lignes_disponibles.toLocaleString("fr-FR")} lignes
      </p>

      <KpiCards kpi={analysis.kpi} />

      <div className="charts-row">
        <div className="card">
          <h3>Répartition des statuts</h3>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie
                data={analysis.repartition_statuts}
                dataKey="nombre"
                nameKey="statut"
                outerRadius={90}
                label={(e) => `${e.statut}: ${e.nombre}`}
              >
                {analysis.repartition_statuts.map((entry) => (
                  <Cell key={entry.statut} fill={COLORS[entry.statut] || "#94a3b8"} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h3>Évolution par date de chargement</h3>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={analysis.evolution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date_chargement" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="nombre" stroke="#6366f1" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <h3>Détail des fiches ({total.toLocaleString("fr-FR")})</h3>
        <div className="filters-bar">
          <select
            value={filters.statut}
            onChange={(e) => setFilters((f) => ({ ...f, statut: e.target.value }))}
          >
            <option value="">Tous les statuts</option>
            {Object.keys(COLORS).map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <select
            value={filters.code_marketing}
            onChange={(e) => setFilters((f) => ({ ...f, code_marketing: e.target.value }))}
          >
            <option value="">Tous les codes marketing</option>
            {codesMarketing.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <input
            type="text"
            placeholder="Date de chargement"
            value={filters.date_chargement}
            onChange={(e) => setFilters((f) => ({ ...f, date_chargement: e.target.value }))}
          />
          <a className="primary" style={{ textDecoration: "none" }}
             href={exportUrl(analysis.analysis_id, "csv", filters.statut)}>
            <button className="primary">Export CSV</button>
          </a>
          <a style={{ textDecoration: "none" }}
             href={exportUrl(analysis.analysis_id, "xlsx", filters.statut)}>
            <button className="primary">Export Excel</button>
          </a>
        </div>

        <table>
          <thead>
            <tr>
              {["contact_date_fiche", "date_chargement", "contact_qualif1", "code_marketing", "nbr_appel", "priorite", "statut_affichage"].map((col) => (
                <th key={col} onClick={() => toggleSort(col)}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedFiches.slice(0, 500).map((f, i) => (
              <tr key={i}>
                <td>{f.contact_date_fiche}</td>
                <td>{f.date_chargement}</td>
                <td>{f.contact_qualif1}</td>
                <td>{f.code_marketing}</td>
                <td>{f.nbr_appel}</td>
                <td>{f.priorite}</td>
                <td><span className={`tag ${TAG_CLASS[f.statut_affichage] || ""}`}>{f.statut_affichage}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
        {total > 500 && <p style={{ color: "#64748b" }}>Affichage des 500 premières lignes sur {total}. Utilisez les filtres ou l'export pour la totalité.</p>}
      </div>
    </div>
  );
}
