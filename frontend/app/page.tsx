"use client";

import { useState } from "react";

const secteurs = ["Marketing", "Finance", "Ressources Humaines", "Technologie", "Santé", "Éducation", "Commerce", "Industrie", "Autre"];
const tailles = ["1-10 employés", "11-50 employés", "51-200 employés", "201-500 employés", "500+ employés"];
const budgets = ["0 - 500$", "500 - 2 000$", "2 000 - 5 000$", "5 000 - 10 000$", "10 000 - 25 000$", "25 000$+"];
const defis = [
  "Manque d'automatisation", "Difficile d’analyser les données", "Problème de gestion des leads/ventes",
  "Service client inefficace", "Trop de tâches répétitives", "Manque de visibilité sur le marché",
  "Difficile de personnaliser l’offre pour les clients", "Mauvaise gestion des stocks/logistique",
  "Sécurité et conformité des données", "Manque d'innovation dans l'entreprise"
];
const objectifs = [
  "Augmenter les ventes", "Automatiser les tâches internes", "Améliorer l’expérience client", "Réduire les coûts opérationnels",
  "Gagner du temps dans les processus internes", "Optimiser le marketing et la publicité", "Personnaliser l’offre pour les clients",
  "Prédire les tendances du marché", "Améliorer la prise de décision avec les données", "Sécuriser les données et automatiser la conformité"
];

export default function DiagnosticForm() {
  const [formData, setFormData] = useState<{ [key: string]: any }>({
    nom_entreprise: "",
    email: "",
    secteur_activite: "",
    taille_entreprise: "",
    defis: [],
    objectifs: [],
    budget: "",
    experience_ia: false,
    outils_ia_utilises: "",
    besoin_ia: "",
    besoin_ia_principal: ""
  });

  const [diagnostic, setDiagnostic] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [leadEmail, setLeadEmail] = useState("");
  const [emailConfirmed, setEmailConfirmed] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type, checked } = e.target;

    setFormData((prevData) => {
      if (type === "checkbox") {
        const prevValues = Array.isArray(prevData[name]) ? prevData[name] : [];
        return {
          ...prevData,
          [name]: checked ? [...prevValues, value] : prevValues.filter((v) => v !== value),
        };
      }

      return { ...prevData, [name]: value };
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/diagnostic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la soumission du formulaire");
      }

      const data = await response.json();
      setDiagnostic(data.diagnostic);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded">
      <h2 className="text-xl font-semibold mb-4">Diagnostic IA</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="nom_entreprise" placeholder="Nom de l'entreprise" value={formData.nom_entreprise} onChange={handleChange} className="border p-2 rounded w-full mb-2" />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} className="border p-2 rounded w-full mb-2" />
        
        <select name="secteur_activite" value={formData.secteur_activite} onChange={handleChange} className="border p-2 rounded w-full mb-2">
          <option value="">Secteur d'activité</option>
          {secteurs.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        
        <select name="taille_entreprise" value={formData.taille_entreprise} onChange={handleChange} className="border p-2 rounded w-full mb-2">
          <option value="">Taille de l'entreprise</option>
          {tailles.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>

        <fieldset className="mb-2">
          <legend className="font-semibold">Défis</legend>
          {defis.map((d) => (
            <label key={d} className="block">
              <input type="checkbox" name="defis" value={d} onChange={handleChange} /> {d}
            </label>
          ))}
        </fieldset>

        <fieldset className="mb-2">
          <legend className="font-semibold">Objectifs</legend>
          {objectifs.map((o) => (
            <label key={o} className="block">
              <input type="checkbox" name="objectifs" value={o} onChange={handleChange} /> {o}
            </label>
          ))}
        </fieldset>

        <select name="budget" value={formData.budget} onChange={handleChange} className="border p-2 rounded w-full mb-2">
          <option value="">Budget</option>
          {budgets.map((b) => <option key={b} value={b}>{b}</option>)}
        </select>

        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">
            Quel serait votre principal besoin en IA ?
          </label>
          <textarea
            name="besoin_ia_principal"
            placeholder="Décrivez ici votre besoin IA principal..."
            value={formData.besoin_ia_principal}
            onChange={handleChange}
            className="border p-2 rounded w-full h-24"
          />
        </div>

        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded w-full mt-4" disabled={loading}>
          {loading ? "Analyse en cours..." : "Soumettre"}
        </button>
      </form>

      {error && <p className="text-red-500 mt-4">{error}</p>}
      {diagnostic && <p className="mt-4">{diagnostic}</p>}
    </div>
  );
}
