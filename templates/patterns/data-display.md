# Pattern: Data Display
<!-- Derived from shadcn-ui/ui (MIT License) & wshobson/agents (MIT License) -->

Deterministic components for high-density tabular metrics, telemetry, and structured records without artificial AI ornamentation.

## 1. High-Density Cockpit Architectural Rules

### Data Preservation Mandate (정보 생략 금지)
- **밀도(Density) != 미니멀리즘**: 고밀도는 정보를 비우는 것이 아니라, 단위 면적당 수용 가능한 텔레메트리 정보량을 극대화하는 것이다.
- 24/7 관제 도구에서 Load average (1m/5m/15m), Swap margin, Rx/Tx split, 스파크라인 등 핵심 커널/인프라 텔레메트리를 절대 생략하지 않는다.
- 단일 셀 내에 **Primary Metric + Slim Gauge + Secondary Metric**을 3단 복합 수납(Multi-Metric Cell)하여 화면 높이와 가로폭을 효율적으로 사용한다.

### Layout & Sizing Rules
- **`max-w-7xl` 인위적 폭 제한 금지**: B2B 관제 대시보드에서는 `max-w-7xl`, `max-w-6xl` 등의 래퍼를 전면 금지하고 `w-full` 전폭 확장을 적용한다. 1440px+ 뷰포트에서 좌우 160px+ 여백 방치를 차단한다.
- **단일 뷰포트 스크롤 0px 지향**: 1440x900 뷰포트 기준, 불필요한 전체 페이지 스크롤 없이 단일 화면(Single-Screen Cockpit) 내에 전체 노드와 핵심 지표를 100% 수납할 수 있도록 수직 리듬(py-2~2.5)을 콤팩트하게 통제한다.

### Alignment & Ordering Rules
- **수치 우측 정렬 (Numeric Right-Alignment)**: 모든 정량적 수치 데이터(헤더 `<th>`, 셀 `<td>`, 게이지 수치)는 자릿수 비교 가독성을 위해 반드시 `text-right` 및 `justify-end`를 적용한다.
- **심각도 우선 정렬 (Severity-First Ordering)**: 장애 인지 시간(MTTD) 최소화를 위해 인프라 노드는 상태 심각도순(`CRITICAL` -> `WARNING` -> `NORMAL` -> `OFFLINE`/`MAINTENANCE`)을 기본 정렬 기준으로 적용한다.

---

## 2. High-Density Multi-Metric Table with Full 4-State Coverage

Hobson 4-State Contract (Loading Skeleton, Actionable Error, Actionable Empty, Populated)를 100% 준수하며 복합 커널 메트릭을 수납하는 고밀도 테이블 컴포넌트입니다.

```tsx
"use client";

import React, { useMemo, useState } from "react";
import { AlertCircle, RefreshCw, Server, ShieldAlert } from "lucide-react";

export type HealthSeverity = "CRITICAL" | "WARNING" | "NORMAL" | "OFFLINE";

export interface TelemetryNodeRecord {
  id: string;
  name: string;
  role: string;
  ip: string;
  region: string;
  status: HealthSeverity;
  statusLabel: string;
  cpu: {
    usagePercent: number;
    cores: number;
    loadAvg: [number, number, number];
  };
  memory: {
    usedGb: number;
    totalGb: number;
    usagePercent: number;
    swapMarginPercent: number;
  };
  disk: {
    totalIops: number;
  };
  network: {
    rxMbps: number;
    txMbps: number;
  };
  uptime: string;
  uptimePercent: number;
}

const SEVERITY_WEIGHT: Record<HealthSeverity, number> = {
  CRITICAL: 4,
  WARNING: 3,
  NORMAL: 2,
  OFFLINE: 1,
};

const STATUS_BADGE_STYLE: Record<
  HealthSeverity,
  { label: string; bg: string; text: string; dot: string; border: string }
> = {
  CRITICAL: {
    label: "임계",
    bg: "bg-status-error-bg",
    text: "text-status-error",
    dot: "bg-status-error animate-pulse",
    border: "border-status-error-border",
  },
  WARNING: {
    label: "주의",
    bg: "bg-status-warning-bg",
    text: "text-status-warning",
    dot: "bg-status-warning",
    border: "border-status-warning-border",
  },
  NORMAL: {
    label: "정상",
    bg: "bg-status-success-bg",
    text: "text-status-success",
    dot: "bg-status-success",
    border: "border-status-success-border",
  },
  OFFLINE: {
    label: "오프라인",
    bg: "bg-surface-secondary",
    text: "text-muted",
    dot: "bg-muted",
    border: "border-border",
  },
};

function getBarColor(percent: number, status: HealthSeverity): string {
  if (status === "OFFLINE") return "bg-muted";
  if (percent >= 85) return "bg-status-error";
  if (percent >= 70) return "bg-status-warning";
  return "bg-accent";
}

export interface DenseTelemetryTableProps {
  nodes: TelemetryNodeRecord[];
  isLoading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  onResetFilters?: () => void;
}

export function DenseTelemetryTable({
  nodes,
  isLoading = false,
  error = null,
  onRetry,
  onResetFilters,
}: DenseTelemetryTableProps) {
  const [sortField, setSortField] = useState<"severity" | "cpu" | "memory" | "uptime">("severity");
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  // Severity-first default sort
  const sortedNodes = useMemo(() => {
    return [...nodes].sort((a, b) => {
      let diff = 0;
      if (sortField === "severity") {
        diff = SEVERITY_WEIGHT[a.status] - SEVERITY_WEIGHT[b.status];
      } else if (sortField === "cpu") {
        diff = a.cpu.usagePercent - b.cpu.usagePercent;
      } else if (sortField === "memory") {
        diff = a.memory.usagePercent - b.memory.usagePercent;
      } else if (sortField === "uptime") {
        diff = a.uptimePercent - b.uptimePercent;
      }
      return sortAsc ? diff : -diff;
    });
  }, [nodes, sortField, sortAsc]);

  const toggleSort = (field: "severity" | "cpu" | "memory" | "uptime") => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  return (
    <div className="w-full border border-border rounded-lg bg-surface shadow-elevation-1 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-sans border-collapse" role="table">
          <thead>
            <tr className="border-b border-border bg-surface-secondary text-muted font-medium select-none">
              <th scope="col" className="py-2.5 px-3 text-left">호스트 인스턴스</th>
              <th scope="col" className="py-2.5 px-3 text-left font-mono">IP / 리전</th>
              <th
                scope="col"
                onClick={() => toggleSort("severity")}
                className="py-2.5 px-3 text-center cursor-pointer hover:text-foreground"
              >
                헬스 상태
              </th>
              <th
                scope="col"
                onClick={() => toggleSort("cpu")}
                className="py-2.5 px-3 text-right cursor-pointer hover:text-foreground min-w-[170px]"
              >
                CPU 부하율 (부하 바 / 로드)
              </th>
              <th
                scope="col"
                onClick={() => toggleSort("memory")}
                className="py-2.5 px-3 text-right cursor-pointer hover:text-foreground min-w-[170px]"
              >
                메모리 점유율 (스왑 여유)
              </th>
              <th scope="col" className="py-2.5 px-3 text-right font-mono min-w-[150px]">
                디스크 IOPS / Throughput
              </th>
              <th
                scope="col"
                onClick={() => toggleSort("uptime")}
                className="py-2.5 px-3 text-right cursor-pointer hover:text-foreground min-w-[110px]"
              >
                가동 시간 (Uptime)
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-border-subtle" aria-busy={isLoading}>
            {isLoading ? (
              // 1. Loading Skeleton State
              Array.from({ length: 7 }).map((_, idx) => (
                <tr key={`skeleton-${idx}`} className="animate-pulse">
                  <td className="py-2.5 px-3">
                    <div className="h-3.5 w-32 bg-skeleton rounded" />
                    <div className="h-2.5 w-20 bg-skeleton-subtle rounded mt-1" />
                  </td>
                  <td className="py-2.5 px-3">
                    <div className="h-3 w-24 bg-skeleton-subtle rounded" />
                  </td>
                  <td className="py-2.5 px-3 text-center">
                    <div className="h-4 w-12 bg-skeleton rounded mx-auto" />
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <div className="h-3 w-20 bg-skeleton rounded ml-auto" />
                    <div className="h-1.5 w-full bg-skeleton rounded mt-1" />
                    <div className="h-2 w-28 bg-skeleton-subtle rounded mt-1 ml-auto" />
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <div className="h-3 w-20 bg-skeleton rounded ml-auto" />
                    <div className="h-1.5 w-full bg-skeleton rounded mt-1" />
                    <div className="h-2 w-24 bg-skeleton-subtle rounded mt-1 ml-auto" />
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <div className="h-3 w-16 bg-skeleton rounded ml-auto" />
                    <div className="h-2 w-28 bg-skeleton-subtle rounded mt-1 ml-auto" />
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <div className="h-3 w-16 bg-skeleton rounded ml-auto" />
                  </td>
                </tr>
              ))
            ) : error ? (
              // 2. Actionable Error Recovery State
              <tr role="alert">
                <td colSpan={7} className="py-10 px-4 text-center">
                  <div className="flex flex-col items-center justify-center max-w-sm mx-auto">
                    <span className="p-2.5 rounded-full bg-status-error-bg text-status-error border border-status-error-border mb-2.5">
                      <ShieldAlert className="w-5 h-5" aria-hidden="true" />
                    </span>
                    <h4 className="text-sm font-semibold text-foreground">
                      텔레메트리 데이터 파이프라인 수집 오류
                    </h4>
                    <p className="text-xs text-muted mt-1 leading-relaxed">{error}</p>
                    {onRetry && (
                      <button
                        type="button"
                        onClick={onRetry}
                        className="mt-3.5 inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded bg-surface border border-border text-foreground hover:bg-surface-secondary active:scale-95 transition-colors"
                      >
                        <RefreshCw className="w-3.5 h-3.5 text-muted" aria-hidden="true" />
                        수집 파이프라인 재시도
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ) : sortedNodes.length === 0 ? (
              // 3. Actionable Zero-Data Empty State
              <tr>
                <td colSpan={7} className="py-12 px-4 text-center">
                  <div className="flex flex-col items-center justify-center max-w-sm mx-auto">
                    <span className="p-2.5 rounded-full bg-background border border-border text-muted mb-2.5">
                      <Server className="w-5 h-5" aria-hidden="true" />
                    </span>
                    <h4 className="text-sm font-semibold text-foreground">
                      일치하는 텔레메트리 노드가 없습니다
                    </h4>
                    <p className="text-xs text-muted mt-1">
                      검색 필터 조건에 부합하는 클러스터 노드가 없습니다.
                    </p>
                    {onResetFilters && (
                      <button
                        type="button"
                        onClick={onResetFilters}
                        className="mt-3.5 px-3 py-1.5 text-xs font-medium rounded bg-accent text-background hover:opacity-90 active:scale-95 transition-opacity"
                      >
                        전체 필터로 복원
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ) : (
              // 4. Populated Records with Multi-Metric Cells
              sortedNodes.map((node) => {
                const statusCfg = STATUS_BADGE_STYLE[node.status];
                const cpuBar = getBarColor(node.cpu.usagePercent, node.status);
                const memBar = getBarColor(node.memory.usagePercent, node.status);

                return (
                  <tr
                    key={node.id}
                    className="hover:bg-surface-secondary/70 transition-colors duration-fast group"
                  >
                    {/* 호스트 인스턴스 */}
                    <td className="py-2.5 px-3">
                      <div className="font-semibold text-foreground truncate max-w-[200px]" title={node.name}>
                        {node.name}
                      </div>
                      <div className="text-[11px] text-muted truncate max-w-[210px] mt-0.5">
                        {node.role}
                      </div>
                    </td>

                    {/* IP / 리전 */}
                    <td className="py-2.5 px-3">
                      <span className="font-mono text-foreground font-medium bg-background px-1.5 py-0.5 rounded border border-border">
                        {node.ip}
                      </span>
                      <div className="text-[10px] text-muted mt-0.5">{node.region}</div>
                    </td>

                    {/* 헬스 상태 */}
                    <td className="py-2.5 px-3 text-center">
                      <span
                        className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-mono font-medium border ${statusCfg.bg} ${statusCfg.text} ${statusCfg.border}`}
                      >
                        <span className={`w-1.5 h-1.5 rounded-full ${statusCfg.dot}`} />
                        <span>{node.statusLabel}</span>
                      </span>
                    </td>

                    {/* CPU 복합 셀 (Primary + Slim Gauge + Secondary Load Avg) */}
                    <td className="py-2.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-1.5 font-mono text-[11px]">
                        <span className="font-semibold text-foreground">
                          {node.cpu.usagePercent.toFixed(1)}%
                        </span>
                        <span className="text-[10px] text-muted font-sans">
                          ({node.cpu.cores}C)
                        </span>
                      </div>
                      <div className="w-full bg-background rounded-full h-1 overflow-hidden my-1 border border-border-subtle">
                        <div
                          className={`h-full rounded-full transition-all duration-normal ${cpuBar}`}
                          style={{ width: `${Math.min(node.cpu.usagePercent, 100)}%` }}
                        />
                      </div>
                      <div className="text-[10px] text-muted font-mono">
                        로드: {node.cpu.loadAvg.join(" · ")}
                      </div>
                    </td>

                    {/* 메모리 복합 셀 (Primary + Slim Gauge + Secondary Swap) */}
                    <td className="py-2.5 px-3 text-right">
                      <div className="flex items-center justify-end gap-1.5 font-mono text-[11px]">
                        <span className="font-semibold text-foreground">
                          {node.memory.usagePercent.toFixed(1)}%
                        </span>
                        <span className="text-[10px] text-muted font-sans">
                          ({node.memory.usedGb}G/{node.memory.totalGb}G)
                        </span>
                      </div>
                      <div className="w-full bg-background rounded-full h-1 overflow-hidden my-1 border border-border-subtle">
                        <div
                          className={`h-full rounded-full transition-all duration-normal ${memBar}`}
                          style={{ width: `${Math.min(node.memory.usagePercent, 100)}%` }}
                        />
                      </div>
                      <div className="text-[10px] text-muted font-mono">
                        스왑 여유: {node.memory.swapMarginPercent.toFixed(1)}%
                      </div>
                    </td>

                    {/* 디스크 IOPS & 네트워크 Throughput (Rx/Tx Split) */}
                    <td className="py-2.5 px-3 text-right font-mono text-xs">
                      <div className="text-foreground">
                        {node.disk.totalIops.toLocaleString()}{" "}
                        <span className="text-[10px] text-muted font-sans">IOPS</span>
                      </div>
                      <div className="text-[10px] text-muted mt-0.5">
                        Rx {(node.network.rxMbps / 1000).toFixed(1)}G / Tx{" "}
                        {(node.network.txMbps / 1000).toFixed(1)}G
                      </div>
                    </td>

                    {/* 가동 시간 (Uptime) */}
                    <td className="py-2.5 px-3 text-right">
                      <div className="font-medium text-foreground">{node.uptime}</div>
                      <div className="text-[10px] text-muted font-mono mt-0.5">
                        가용률 {node.uptimePercent}%
                      </div>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

---

## 3. Telemetry Metric Card with Embedded Sparkline

A/B 벤치마크에서 입증된 시계열 트렌드 스파크라인(인라인 SVG)과 다크 팔레트 토큰 바인딩을 적용한 메트릭 카드입니다.

```tsx
"use client";

import React from "react";
import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";

export interface TelemetryMetricCardProps {
  title: string;
  value: string;
  unit: string;
  changeRate: number;
  changePeriod: string;
  status: "NORMAL" | "WARNING" | "CRITICAL";
  statusLabel: string;
  sparkline: number[];
  description: string;
}

export function TelemetryMetricCard({
  title,
  value,
  unit,
  changeRate,
  changePeriod,
  status,
  statusLabel,
  sparkline,
  description,
}: TelemetryMetricCardProps) {
  // Mini SVG Sparkline calculation
  const minVal = Math.min(...sparkline);
  const maxVal = Math.max(...sparkline);
  const range = maxVal - minVal || 1;
  const points = sparkline
    .map((val, idx) => {
      const x = (idx / (sparkline.length - 1)) * 100;
      const y = 26 - ((val - minVal) / range) * 20;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");

  const strokeColorClass =
    status === "CRITICAL"
      ? "text-status-error"
      : status === "WARNING"
      ? "text-status-warning"
      : "text-accent";

  return (
    <article className="p-3.5 border border-border rounded-lg bg-surface shadow-elevation-1 hover:border-border-strong transition-colors duration-fast flex flex-col justify-between">
      {/* Title & Status Badge */}
      <header className="flex items-center justify-between gap-2">
        <h3 className="text-xs font-medium text-muted truncate">{title}</h3>
        <span
          className={`px-1.5 py-0.5 text-[11px] font-mono font-medium rounded border ${
            status === "CRITICAL"
              ? "bg-status-error-bg text-status-error border-status-error-border"
              : status === "WARNING"
              ? "bg-status-warning-bg text-status-warning border-status-warning-border"
              : "bg-status-success-bg text-status-success border-status-success-border"
          }`}
        >
          {statusLabel}
        </span>
      </header>

      {/* Metric Value & Delta */}
      <div className="mt-2.5 flex items-baseline justify-between gap-2">
        <div className="flex items-baseline gap-1 font-mono">
          <span className="text-2xl font-bold tracking-tight text-foreground">{value}</span>
          <span className="text-xs text-muted">{unit}</span>
        </div>

        <div className="flex items-center gap-1 font-mono text-xs">
          {changeRate === 0 ? (
            <span className="flex items-center text-muted">
              <Minus className="w-3.5 h-3.5" /> 0.0%
            </span>
          ) : changeRate > 0 ? (
            <span className="flex items-center text-status-error font-medium">
              <ArrowUpRight className="w-3.5 h-3.5 stroke-[2.5]" /> +{changeRate}%
            </span>
          ) : (
            <span className="flex items-center text-status-success font-medium">
              <ArrowDownRight className="w-3.5 h-3.5 stroke-[2.5]" /> {changeRate}%
            </span>
          )}
          <span className="text-[10px] text-muted font-sans">{changePeriod}</span>
        </div>
      </div>

      {/* Sparkline & Sub-description footer */}
      <footer className="mt-2.5 pt-2 border-t border-border-subtle flex items-center justify-between gap-2">
        <p className="text-[11px] text-muted truncate flex-1">{description}</p>
        <div className={`w-16 h-5 shrink-0 ${strokeColorClass}`}>
          <svg className="w-full h-full overflow-visible" viewBox="0 0 100 28">
            <polyline
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={points}
            />
          </svg>
        </div>
      </footer>
    </article>
  );
}
