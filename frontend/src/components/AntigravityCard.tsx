"use client";

import React, { useRef, useEffect, useState, useCallback } from "react";

interface AntigravityCardProps {
  tripId: string;
  vendor: string;
  claimedFare: string;
  computedFare: string;
  delta: string;
  verdict: "DISCREPANCY" | "MATCH" | "CANNOT_DETERMINE";
  clauseId: string;
  onInspect: (tripId: string) => void;
  onDispute?: () => void;
}

interface PhysicsState {
  x: number;
  y: number;
  vx: number;
  vy: number;
  targetX: number;
  targetY: number;
}

export const AntigravityCard: React.FC<AntigravityCardProps> = ({
  tripId,
  vendor,
  claimedFare,
  computedFare,
  delta,
  verdict,
  clauseId,
  onInspect,
  onDispute,
}) => {
  const cardRef = useRef<HTMLDivElement | null>(null);

  // Kinetic & Spatial Physics Constants
  const MASS = 0.45; // Low-medium mass (buoyant operational plane)
  const STIFFNESS = 180.0; // Hooke's spring constant (k)
  const DAMPING = 16.5; // Viscous damping resistance (c)
  const REPEL_RADIUS = 95.0; // Dynamic proximity force field (px)
  const REPEL_FORCE = 1400.0; // Repulsion amplitude
  const LEVITATE_AMP = 3.5; // Ambient vertical float amplitude (px)
  const LEVITATE_FREQ = 0.0022; // Harmonic levitation frequency

  const [isReducedMotion, setIsReducedMotion] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  // Physics vectors maintained in mutable ref for 60/120fps GPU performance
  const physics = useRef<PhysicsState>({
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    targetX: 0,
    targetY: 0,
  });

  const pointer = useRef<{ x: number; y: number; active: boolean }>({
    x: -9999,
    y: -9999,
    active: false,
  });

  const dragStart = useRef<{ mouseX: number; mouseY: number; initialX: number; initialY: number }>({
    mouseX: 0,
    mouseY: 0,
    initialX: 0,
    initialY: 0,
  });

  const animFrameId = useRef<number>(0);
  const lastTime = useRef<number>(0);

  // Reduced motion preference detection
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setIsReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsReducedMotion(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  // Main 120fps Physics Simulation Loop
  const updatePhysics = useCallback(
    (timestamp: number) => {
      if (!lastTime.current) lastTime.current = timestamp;
      const dt = Math.min((timestamp - lastTime.current) / 1000, 0.032);
      lastTime.current = timestamp;

      const p = physics.current;
      const cardEl = cardRef.current;

      if (!cardEl || isReducedMotion) {
        return;
      }

      if (!isDragging) {
        // 1. Ambient Sinusoidal Levitation
        const ambientFloatY = Math.sin(timestamp * LEVITATE_FREQ) * LEVITATE_AMP;

        // 2. Cursor Proximity Force Field
        let repelFx = 0;
        let repelFy = 0;

        if (pointer.current.active && !isHovered) {
          const rect = cardEl.getBoundingClientRect();
          const cardCenterX = rect.left + rect.width / 2;
          const cardCenterY = rect.top + rect.height / 2;

          const dx = pointer.current.x - cardCenterX;
          const dy = pointer.current.y - cardCenterY;
          const dist = Math.hypot(dx, dy);

          if (dist < REPEL_RADIUS && dist > 1.0) {
            const factor = Math.exp(-(dist * dist) / (2 * (REPEL_RADIUS / 2) ** 2));
            const force = (REPEL_FORCE * factor) / dist;
            repelFx = -dx * force;
            repelFy = -dy * force;
          }
        }

        // 3. Hooke's Law Spring Force
        const springFx = -STIFFNESS * (p.x - p.targetX);
        const springFy = -STIFFNESS * (p.y - (p.targetY + ambientFloatY));

        // 4. Viscous Damping Resistance Force
        const dampFx = -DAMPING * p.vx;
        const dampFy = -DAMPING * p.vy;

        // 5. Numerical Integration (Semi-Implicit Euler)
        const ax = (springFx + dampFx + repelFx) / MASS;
        const ay = (springFy + dampFy + repelFy) / MASS;

        p.vx += ax * dt;
        p.vy += ay * dt;

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        // 6. Direct Hardware-Accelerated GPU Transform
        cardEl.style.transform = `translate3d(${p.x.toFixed(2)}px, ${p.y.toFixed(2)}px, 0px) scale(${
          isHovered ? 1.02 : 1.0
        })`;
      }

      animFrameId.current = requestAnimationFrame(updatePhysics);
    },
    [isDragging, isHovered, isReducedMotion]
  );

  useEffect(() => {
    if (isReducedMotion) return;
    animFrameId.current = requestAnimationFrame(updatePhysics);
    return () => cancelAnimationFrame(animFrameId.current);
  }, [updatePhysics, isReducedMotion]);

  // Global pointer tracking for proximity deflection
  useEffect(() => {
    const handleGlobalPointerMove = (e: PointerEvent) => {
      pointer.current.x = e.clientX;
      pointer.current.y = e.clientY;
      pointer.current.active = true;
    };

    const handlePointerLeaveWindow = () => {
      pointer.current.active = false;
    };

    window.addEventListener("pointermove", handleGlobalPointerMove, { passive: true });
    window.addEventListener("pointerout", handlePointerLeaveWindow, { passive: true });
    return () => {
      window.removeEventListener("pointermove", handleGlobalPointerMove);
      window.removeEventListener("pointerout", handlePointerLeaveWindow);
    };
  }, []);

  // Pointer Drag Handlers
  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    dragStart.current = {
      mouseX: e.clientX,
      mouseY: e.clientY,
      initialX: physics.current.x,
      initialY: physics.current.y,
    };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    const dx = e.clientX - dragStart.current.mouseX;
    const dy = e.clientY - dragStart.current.mouseY;

    physics.current.x = dragStart.current.initialX + dx;
    physics.current.y = dragStart.current.initialY + dy;
    physics.current.vx = 0;
    physics.current.vy = 0;

    if (cardRef.current) {
      cardRef.current.style.transform = `translate3d(${physics.current.x.toFixed(2)}px, ${physics.current.y.toFixed(
        2
      )}px, 0px) scale(1.03)`;
    }
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    setIsDragging(false);
    try {
      (e.target as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      // Ignore if released
    }

    // Snap back to equilibrium with smooth spring
    physics.current.targetX = 0;
    physics.current.targetY = 0;
  };

  return (
    <div
      ref={cardRef}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onPointerCancel={handlePointerUp}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onFocus={() => {
        // Freeze physics on keyboard focus for WCAG accessibility
        physics.current.x = 0;
        physics.current.y = 0;
        physics.current.vx = 0;
        physics.current.vy = 0;
      }}
      tabIndex={0}
      role="article"
      aria-label={`Audit result for Trip ${tripId}, ${verdict}, delta of ${delta} rupees`}
      className={`relative select-none cursor-grab active:cursor-grabbing p-4 rounded-2xl border transition-shadow duration-300 ${
        verdict === "DISCREPANCY"
          ? "bg-slate-900/90 border-rose-500/40 shadow-lg shadow-rose-950/20"
          : verdict === "MATCH"
          ? "bg-slate-900/90 border-emerald-500/40 shadow-lg shadow-emerald-950/20"
          : "bg-slate-900/90 border-amber-500/40 shadow-lg shadow-amber-950/20"
      } backdrop-blur-md will-change-transform focus:outline-none focus:ring-2 focus:ring-emerald-400`}
      style={{
        touchAction: "none",
      }}
    >
      {/* Top Header: Floating Status Bubble */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2">
          <span
            className={`w-2.5 h-2.5 rounded-full ${
              verdict === "DISCREPANCY"
                ? "bg-rose-500 animate-pulse"
                : verdict === "MATCH"
                ? "bg-emerald-400"
                : "bg-amber-400"
            }`}
          />
          <span className="font-mono font-bold text-xs text-white tracking-wider">{tripId}</span>
          <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded-md font-sans border border-slate-700">
            {vendor}
          </span>
        </div>
        <span
          className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
            verdict === "DISCREPANCY"
              ? "bg-rose-500/10 text-rose-300 border border-rose-500/30"
              : verdict === "MATCH"
              ? "bg-emerald-500/10 text-emerald-300 border border-emerald-500/30"
              : "bg-amber-500/10 text-amber-300 border border-amber-500/30"
          }`}
        >
          {verdict}
        </span>
      </div>

      {/* Financial Comparison Ground */}
      <div className="grid grid-cols-3 gap-2 bg-slate-950/80 p-2.5 rounded-xl border border-slate-800/80 text-center font-mono">
        <div>
          <div className="text-[9px] uppercase tracking-wider text-slate-400">Claimed</div>
          <div className="text-xs font-bold text-slate-200 mt-0.5">₹{claimedFare}</div>
        </div>
        <div>
          <div className="text-[9px] uppercase tracking-wider text-slate-400">Rate Card</div>
          <div className="text-xs font-bold text-emerald-400 mt-0.5">₹{computedFare}</div>
        </div>
        <div>
          <div className="text-[9px] uppercase tracking-wider text-slate-400">Delta</div>
          <div
            className={`text-xs font-bold mt-0.5 ${
              verdict === "DISCREPANCY" ? "text-rose-400" : "text-emerald-400"
            }`}
          >
            {verdict === "DISCREPANCY" ? `+₹${delta}` : "₹0.00"}
          </div>
        </div>
      </div>

      {/* Footer & Deep-Dive Trigger */}
      <div className="mt-3 flex items-center justify-between pt-2 border-t border-slate-800/60 text-[10px]">
        <span className="text-slate-400 font-mono truncate max-w-[130px]">{clauseId}</span>
        <div className="flex gap-1.5">
          {verdict === "DISCREPANCY" && onDispute && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDispute();
              }}
              className="px-2 py-1 rounded bg-rose-950 hover:bg-rose-900 text-rose-300 font-semibold border border-rose-800/60 transition"
              title="1-Click Dispute Ticket"
            >
              Dispute 📋
            </button>
          )}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onInspect(tripId);
            }}
            className="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold transition shadow-sm"
          >
            Inspect →
          </button>
        </div>
      </div>
    </div>
  );
};
