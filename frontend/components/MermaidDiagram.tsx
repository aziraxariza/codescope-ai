"use client";

import { useEffect, useRef } from "react";

interface Props {
  chart: string;
}

export default function MermaidDiagram({ chart }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || !chart) return;

    let cancelled = false;

    async function render() {
      const mermaid = (await import("mermaid")).default;
      mermaid.initialize({
        startOnLoad: false,
        theme: "dark",
        themeVariables: {
          primaryColor: "#1d9e75",
          primaryTextColor: "#e8e8ed",
          primaryBorderColor: "#2a2d3a",
          lineColor: "#8b8fa8",
          secondaryColor: "#1a1d27",
          tertiaryColor: "#0f1117",
        },
      });

      try {
        const id = `mermaid-${Date.now()}`;
        const { svg } = await mermaid.render(id, chart);
        if (!cancelled && ref.current) {
          ref.current.innerHTML = svg;
        }
      } catch (err) {
        if (!cancelled && ref.current) {
          ref.current.innerHTML = `<p class="text-red-400 text-sm p-4">Diagram render error. Check the Mermaid syntax.</p>`;
        }
      }
    }

    render();
    return () => { cancelled = true; };
  }, [chart]);

  return (
    <div
      ref={ref}
      className="mermaid-wrap w-full overflow-x-auto rounded-lg bg-[#1a1d27] p-4 min-h-[200px]"
    />
  );
}
