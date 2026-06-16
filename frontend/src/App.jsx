import React, { useState } from "react";
import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import Upload from "./pages/Upload.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import History from "./pages/History.jsx";
import RulesAdmin from "./pages/RulesAdmin.jsx";

export default function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Analyse BDD Fiches</h1>
        <nav>
          <NavLink to="/" end>Upload</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/historique">Historique</NavLink>
          <NavLink to="/regles">Référentiel / Règles</NavLink>
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<Upload onAnalysisReady={setCurrentAnalysis} />} />
          <Route
            path="/dashboard"
            element={
              currentAnalysis ? (
                <Dashboard analysis={currentAnalysis} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route path="/historique" element={<History onSelect={setCurrentAnalysis} />} />
          <Route path="/regles" element={<RulesAdmin />} />
        </Routes>
      </main>
    </div>
  );
}
