"""Gera uma base sintetica agregada de perdas mensais por area."""

from __future__ import annotations

import argparse
from pathlib import Path
import random

import numpy as np
import pandas as pd


DEFAULT_SEED = 42
AREAS = ["Cartões", "Crédito", "Pagamentos", "Investimentos", "Fraudes", "Canais Digitais"]


def generate_perdas(start_month: str, end_month: str, seed: int) -> pd.DataFrame:
    """Gera serie mensal de perdas por area com estatisticas agregadas."""
    rng = np.random.default_rng(seed)
    random.seed(seed)

    months = pd.date_range(start_month, end_month, freq="MS").strftime("%Y-%m").tolist()

    rows = []
    for year_month in months:
        for area in AREAS:
            incidents = int(rng.integers(5, 80))
            total_loss = round(abs(rng.normal(20000, 50000)), 2)
            avg_loss = round(total_loss / incidents, 2)
            median_loss = round(avg_loss * rng.uniform(0.5, 1.2), 2)
            rows.append([year_month, area, incidents, total_loss, avg_loss, median_loss])

    return pd.DataFrame(
        rows,
        columns=[
            "year_month",
            "area",
            "incidents_count",
            "total_loss_brl",
            "avg_loss_brl",
            "median_loss_brl",
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera CSV de perdas mensais por area.")
    parser.add_argument("--start-month", type=str, default="2024-01-01", help="Inicio (YYYY-MM-DD).")
    parser.add_argument("--end-month", type=str, default="2025-12-01", help="Fim (YYYY-MM-DD).")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Seed para reproducibilidade.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "dados" / "perdas_mensais_por_area.csv",
        help="Caminho de saida do CSV.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df_perdas = generate_perdas(start_month=args.start_month, end_month=args.end_month, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df_perdas.to_csv(args.output, index=False)

    print(f"Arquivo gerado: {args.output} ({len(df_perdas)} linhas)")


if __name__ == "__main__":
    main()
