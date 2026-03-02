import { useState, type ChangeEvent, type FormEvent } from "react";
import {
  Scale,
  Gavel,
  Calendar,
  MapPin,
  Building2,
  User,
  Users,
  Clock,
  AlertCircle,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import categories from "./categories.json";

interface PredictionResult {
  predicted_duration_days: number;
  predicted_duration_years: number;
  risk_level: string;
  key_influencing_factors: string[];
}

export default function App() {
  const [formData, setFormData] = useState({
    year: new Date().getFullYear(),
    state_code: "",
    dist_code: "",
    court_no: "",
    judge_position: "",
    female_defendant: "0",
    female_petitioner: "0",
    female_adv_def: "0",
    female_adv_pet: "0",
    type_name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        year: parseInt(formData.year.toString()),
        state_code: parseInt(formData.state_code),
        dist_code: parseInt(formData.dist_code),
        court_no: parseInt(formData.court_no),
        judge_position: formData.judge_position,
        female_defendant: parseInt(formData.female_defendant),
        female_petitioner: parseInt(formData.female_petitioner),
        female_adv_def: parseInt(formData.female_adv_def),
        female_adv_pet: parseInt(formData.female_adv_pet),
        type_name: formData.type_name,
      };

      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("API Error");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white">
            <Scale size={24} />
          </div>
          <h1 className="text-xl font-bold">
            Civic Justice Navigator
          </h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-12 gap-8">

        {/* LEFT: FORM */}
        <div className="lg:col-span-7 bg-white p-6 rounded-xl border border-slate-200 space-y-6">

          <h2 className="font-semibold text-slate-800 flex items-center gap-2">
            <Gavel size={18} className="text-blue-600" />
            Case Details
          </h2>

          <form onSubmit={handleSubmit} className="space-y-5">

            <div className="grid grid-cols-2 gap-4">
              <input type="number" name="year" value={formData.year}
                onChange={handleInputChange}
                className="input" placeholder="Year" required />

              <input type="number" name="state_code"
                value={formData.state_code}
                onChange={handleInputChange}
                className="input" placeholder="State Code" required />

              <input type="number" name="dist_code"
                value={formData.dist_code}
                onChange={handleInputChange}
                className="input" placeholder="District Code" required />

              <input type="number" name="court_no"
                value={formData.court_no}
                onChange={handleInputChange}
                className="input" placeholder="Court No" required />
            </div>

            <select
              name="judge_position"
              value={formData.judge_position}
              onChange={handleInputChange}
              required
              className="input"
            >
              <option value="">Select Judge Position</option>
              {categories.judge_position.map((pos: string) => (
                <option key={pos} value={pos}>{pos}</option>
              ))}
            </select>

            <select
              name="type_name"
              value={formData.type_name}
              onChange={handleInputChange}
              required
              className="input"
            >
              <option value="">Select Case Type</option>
              {categories.type_name.map((type: string) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>

            <div className="grid grid-cols-2 gap-4">
              <SelectField label="Female Defendant" name="female_defendant"
                value={formData.female_defendant} onChange={handleInputChange} />

              <SelectField label="Female Petitioner" name="female_petitioner"
                value={formData.female_petitioner} onChange={handleInputChange} />

              <SelectField label="Female Advocate (Def)" name="female_adv_def"
                value={formData.female_adv_def} onChange={handleInputChange} />

              <SelectField label="Female Advocate (Pet)" name="female_adv_pet"
                value={formData.female_adv_pet} onChange={handleInputChange} />
            </div>

            <button type="submit"
              className="w-full bg-blue-600 text-white py-2.5 rounded-lg flex items-center justify-center gap-2">
              {loading ? <Loader2 className="animate-spin" size={18} /> : <Clock size={18} />}
              Predict Timeline
            </button>

          </form>
        </div>

        {/* RIGHT: RESULT */}
        <div className="lg:col-span-5 bg-white p-6 rounded-xl border border-slate-200 min-h-[300px]">

          {error && <div className="text-red-600 text-sm">{error}</div>}

          {!result && !loading && (
            <div className="text-slate-400 text-center">
              Enter case details to analyze.
            </div>
          )}

          {loading && (
            <div className="text-center">
              <Loader2 className="animate-spin mx-auto text-blue-600" size={40} />
            </div>
          )}

          {result && (
            <div className="space-y-6">

              {/* Duration */}
              <div className="grid grid-cols-2 gap-4">
                <div className="card-blue">
                  {result.predicted_duration_days.toFixed(0)} Days
                </div>
                <div className="card-indigo">
                  {result.predicted_duration_years.toFixed(2)} Years
                </div>
              </div>

              {/* Risk */}
              <div className="text-center">
                <span className={`px-4 py-1.5 rounded-full text-xs font-semibold ${
                  result.risk_level.includes("Low")
                    ? "bg-green-100 text-green-700"
                    : result.risk_level.includes("Moderate")
                    ? "bg-yellow-100 text-yellow-700"
                    : "bg-red-100 text-red-700"
                }`}>
                  {result.risk_level}
                </span>
              </div>

              {/* Explainability */}
              <div>
                <h4 className="text-sm font-semibold mb-2">
                  Key Influencing Factors
                </h4>
                <ul className="text-xs text-slate-600 space-y-1">
                  {result.key_influencing_factors.map((factor, index) => (
                    <li key={index}>
                      • {factor.replace("cat__", "").replace("num__", "")}
                    </li>
                  ))}
                </ul>
              </div>

            </div>
          )}

        </div>
      </main>
    </div>
  );
}

function SelectField({
  label,
  name,
  value,
  onChange,
}: {
  label: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}) {
  return (
    <div>
      <label className="text-sm font-medium">{label}</label>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="input w-full"
      >
        <option value="0">No</option>
        <option value="1">Yes</option>
      </select>
    </div>
  );
}