import { useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

// Greenland Rare Earth Intelligence Dashboard (React)
// Author: Maurice McDonald | Epoch Frameworks LLC
// Data mirrors greenland_ree_deposits.csv. Keep the two in sync.

const WEIGHTS = {
  geological: 0.25,
  regulatory: 0.2,
  ownership: 0.2,
  infrastructure: 0.15,
  geopolitical: 0.2,
};

const DEPOSITS = [
  { name: "Tanbreez (Kringlerne)", resource: 4000, grade: 0.6, hree: 30, owner: "Critical Metals Corp", chinese: 0, status: "Advancing", uranium: 15, geological: 85, regulatory: 90, ownership: 95, infrastructure: 60, geopolitical: 70 },
  { name: "Kvanefjeld", resource: 1010, grade: 1.1, hree: 12, owner: "Energy Transition Minerals", chinese: 9.21, status: "Blocked", uranium: 285, geological: 90, regulatory: 20, ownership: 50, infrastructure: 65, geopolitical: 55 },
  { name: "Sarfartoq", resource: 8.6, grade: 2.0, hree: 15, owner: "Hudson Resources", chinese: 0, status: "Permitted", uranium: 45, geological: 70, regulatory: 75, ownership: 85, infrastructure: 40, geopolitical: 50 },
  { name: "Motzfeldt", resource: 340, grade: 0.25, hree: 8, owner: "Regency Mines", chinese: 0, status: "Exploration", uranium: 60, geological: 55, regulatory: 60, ownership: 80, infrastructure: 55, geopolitical: 40 },
  { name: "Ilímaussaq Complex", resource: 500, grade: 0.8, hree: 18, owner: "Various", chinese: 5, status: "Multiple", uranium: 120, geological: 75, regulatory: 50, ownership: 60, infrastructure: 60, geopolitical: 55 },
  { name: "Tikiusaaq", resource: 25, grade: 1.5, hree: 10, owner: "Unlicensed", chinese: 0, status: "Prospect", uranium: 30, geological: 60, regulatory: 70, ownership: 90, infrastructure: 30, geopolitical: 35 },
  { name: "Qeqertaasaq", resource: 15, grade: 0.9, hree: 12, owner: "Unlicensed", chinese: 0, status: "Prospect", uranium: 25, geological: 50, regulatory: 70, ownership: 90, infrastructure: 20, geopolitical: 30 },
  { name: "Milne Land", resource: 45, grade: 0.65, hree: 8, owner: "GreenRock Resources", chinese: 0, status: "Exploration", uranium: 40, geological: 45, regulatory: 65, ownership: 85, infrastructure: 25, geopolitical: 40 },
  { name: "Niaqornaarsuk", resource: 120, grade: 0.45, hree: 14, owner: "Tanbreez Mining", chinese: 0, status: "Exploration", uranium: 55, geological: 65, regulatory: 70, ownership: 85, infrastructure: 50, geopolitical: 45 },
  { name: "Qaqarssuk", resource: 35, grade: 1.8, hree: 6, owner: "NunaMinerals", chinese: 0, status: "Abandoned", uranium: 20, geological: 55, regulatory: 50, ownership: 80, infrastructure: 35, geopolitical: 30 },
  { name: "Kangerlussuaq", resource: 75, grade: 0.55, hree: 9, owner: "Government", chinese: 0, status: "Reserved", uranium: 35, geological: 50, regulatory: 40, ownership: 70, infrastructure: 45, geopolitical: 50 },
  { name: "Gardar South", resource: 2000, grade: 0.7, hree: 20, owner: "Multiple", chinese: 3, status: "Multiple", uranium: 150, geological: 70, regulatory: 45, ownership: 65, infrastructure: 70, geopolitical: 60 },
  { name: "Narsaq Area", resource: 180, grade: 0.95, hree: 11, owner: "ETM", chinese: 9.21, status: "Uncertain", uranium: 220, geological: 60, regulatory: 30, ownership: 50, infrastructure: 55, geopolitical: 50 },
  { name: "Ivigtut Area", resource: 50, grade: 0.3, hree: 5, owner: "Historical", chinese: 0, status: "Closed", uranium: 15, geological: 30, regulatory: 80, ownership: 85, infrastructure: 60, geopolitical: 20 },
  { name: "Skaergaard", resource: 65, grade: 0.25, hree: 7, owner: "Platina Resources", chinese: 0, status: "PGE Focus", uranium: 10, geological: 40, regulatory: 75, ownership: 80, infrastructure: 35, geopolitical: 25 },
];

const INK = "#2D3436";
const PERIWINKLE = "#8E9FD5";
const PERIWINKLE_DARK = "#6B7FC2";
const RULE = "#E9ECEF";

function composite(d, weights) {
  return Object.entries(weights).reduce((sum, [lens, w]) => sum + d[lens] * w, 0);
}

export default function GreenlandDashboard() {
  const [maxChinese, setMaxChinese] = useState(100);
  const [banLifted, setBanLifted] = useState(false);

  const rows = useMemo(() => {
    return DEPOSITS.filter((d) => d.chinese <= maxChinese).map((d) => {
      const adjusted = { ...d };
      if (banLifted && d.uranium > 100) adjusted.regulatory = Math.min(100, d.regulatory + 40);
      return { ...d, score: Math.round(composite(adjusted, WEIGHTS) * 10) / 10 };
    });
  }, [maxChinese, banLifted]);

  const ranked = useMemo(() => [...rows].sort((a, b) => b.score - a.score), [rows]);
  const western = rows.filter((d) => d.chinese === 0).length;

  return (
    <div style={{ fontFamily: "Georgia, 'Times New Roman', serif", color: INK, maxWidth: 1100, margin: "0 auto", padding: 24 }}>
      <header style={{ borderBottom: `2px solid ${INK}`, paddingBottom: 12, marginBottom: 20 }}>
        <div style={{ fontSize: 13, letterSpacing: 1, color: PERIWINKLE_DARK }}>Open source intelligence</div>
        <h1 style={{ fontSize: 30, margin: "4px 0 6px", fontWeight: 600 }}>Greenland Rare Earth Intelligence</h1>
        <div style={{ fontSize: 15, color: "#636E72" }}>
          {rows.length} deposits shown, {western} under fully Western control. Score follows the five-lens formula in the README.
        </div>
      </header>

      <section style={{ display: "flex", gap: 32, alignItems: "center", marginBottom: 24, fontSize: 15 }}>
        <label>
          Max Chinese stake: <strong>{maxChinese}%</strong>
          <input type="range" min={0} max={100} value={maxChinese} onChange={(e) => setMaxChinese(Number(e.target.value))} style={{ marginLeft: 12, width: 220, accentColor: PERIWINKLE_DARK }} />
        </label>
        <label style={{ cursor: "pointer" }}>
          <input type="checkbox" checked={banLifted} onChange={(e) => setBanLifted(e.target.checked)} style={{ marginRight: 8, accentColor: PERIWINKLE_DARK }} />
          Scenario: uranium ban lifted
        </label>
      </section>

      <section style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>Strategic score by deposit</h2>
        <ResponsiveContainer width="100%" height={420}>
          <BarChart data={ranked} layout="vertical" margin={{ left: 140, right: 24 }}>
            <CartesianGrid stroke={RULE} horizontal={false} />
            <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12 }} />
            <YAxis type="category" dataKey="name" tick={{ fontSize: 12 }} width={140} />
            <Tooltip formatter={(v) => [`${v}`, "Score"]} />
            <Bar dataKey="score" fill={PERIWINKLE} />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>Resource size versus grade</h2>
        <div style={{ fontSize: 13, color: "#636E72", marginBottom: 8 }}>Bubble size is heavy rare earth share. Log scale on resource.</div>
        <ResponsiveContainer width="100%" height={360}>
          <ScatterChart margin={{ left: 12, right: 24, bottom: 12 }}>
            <CartesianGrid stroke={RULE} />
            <XAxis dataKey="resource" type="number" scale="log" domain={["auto", "auto"]} name="Resource (Mt)" tick={{ fontSize: 12 }} label={{ value: "Resource, million tonnes", position: "insideBottom", offset: -6, fontSize: 12 }} />
            <YAxis dataKey="grade" type="number" name="TREO grade (%)" tick={{ fontSize: 12 }} label={{ value: "TREO grade, %", angle: -90, position: "insideLeft", fontSize: 12 }} />
            <ZAxis dataKey="hree" range={[60, 500]} name="Heavy REE (%)" />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} content={({ payload }) => {
              if (!payload || !payload.length) return null;
              const d = payload[0].payload;
              return (
                <div style={{ background: "#fff", border: `1px solid ${RULE}`, padding: 10, fontSize: 13 }}>
                  <div style={{ fontWeight: 600 }}>{d.name}</div>
                  <div>{d.resource} Mt at {d.grade}% TREO, {d.hree}% heavy</div>
                  <div>Score {d.score}, {d.owner}</div>
                </div>
              );
            }} />
            <Legend />
            <Scatter name="Deposits" data={rows} fill={PERIWINKLE_DARK} />
          </ScatterChart>
        </ResponsiveContainer>
      </section>

      <footer style={{ borderTop: `1px solid ${RULE}`, marginTop: 24, paddingTop: 10, fontSize: 12, color: "#636E72" }}>
        Sources: GEUS, USGS MRDS, company filings. Lens scores are analyst judgments; see greenland-strategic-minerals-lens.md.
      </footer>
    </div>
  );
}
