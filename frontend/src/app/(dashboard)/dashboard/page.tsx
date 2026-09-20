"use client";

import { useRouter } from "next/navigation";

const modules = [
  ["Students", "/dashboard/students", "ST"],
  ["Teachers", "/dashboard/teachers", "TC"],
  ["Classes", "/dashboard/classes", "CL"],
  ["Attendance", "/dashboard/attendance", "AT"],
  ["Timetable", "/dashboard/timetable", "TT"],
  ["Exams", "/dashboard/exams", "EX"],
  ["Results", "/dashboard/results", "RS"],
  ["Fees", "/dashboard/fees", "FE"],
  ["Library", "/dashboard/library", "LB"],
  ["Parents", "/dashboard/parents", "PR"],
  ["Reports", "/dashboard/reports", "RP"],
  ["Settings", "/dashboard/settings", "SE"],
] as const;

export default function DashboardPage() {
  const router = useRouter();

  return (
    <main className="min-h-screen bg-slate-950 text-white overflow-hidden">
      <section className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 py-6">
        <header className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-cyan-300">School ERP</p>
            <h1 className="text-2xl font-bold sm:text-3xl">School Command Center</h1>
          </div>
          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-slate-300">
            Main Orbit
          </div>
        </header>

        <div className="flex flex-1 items-center justify-center py-8">
          <div className="relative aspect-square w-full max-w-[720px]">
            <div className="absolute inset-[12%] rounded-full border border-cyan-400/15" />
            <div className="absolute inset-[26%] rounded-full border border-cyan-400/20" />
            <div className="absolute inset-[39%] rounded-full bg-cyan-400/5 blur-2xl" />

            {modules.map(([label, href, short], index) => {
              const angle = (index / modules.length) * Math.PI * 2 - Math.PI / 2;
              const radius = 43;
              const x = 50 + Math.cos(angle) * radius;
              const y = 50 + Math.sin(angle) * radius;
              return (
                <button
                  key={label}
                  type="button"
                  onClick={() => router.push(href)}
                  className="absolute z-20 flex h-[74px] w-[74px] -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border border-cyan-300/25 bg-slate-900/95 p-2 shadow-xl shadow-black/30 transition hover:scale-105 hover:border-cyan-300 focus:outline-none focus:ring-4 focus:ring-cyan-400/30 sm:h-[94px] sm:w-[94px]"
                  style={{ left: `${x}%`, top: `${y}%` }}
                  aria-label={label}
                >
                  <span className="text-sm font-black text-cyan-300 sm:text-base">{short}</span>
                  <span className="mt-1 max-w-full text-[9px] font-semibold leading-tight text-slate-100 sm:text-[11px]">{label}</span>
                </button>
              );
            })}

            <button
              type="button"
              onClick={() => router.push("/dashboard")}
              className="absolute left-1/2 top-1/2 z-30 flex h-[150px] w-[150px] -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border border-cyan-300/40 bg-gradient-to-b from-slate-800 to-slate-950 text-center shadow-2xl shadow-cyan-950/50 focus:outline-none focus:ring-4 focus:ring-cyan-400/30 sm:h-[190px] sm:w-[190px]"
            >
              <span className="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-300">School</span>
              <span className="mt-1 text-2xl font-black sm:text-3xl">ORBIT</span>
              <span className="mt-2 text-[10px] text-slate-400">Tap a module</span>
            </button>
          </div>
        </div>

        <p className="pb-2 text-center text-xs text-slate-500">
          Large tap targets • mobile friendly • one-hand navigation
        </p>
      </section>
    </main>
  );
}
