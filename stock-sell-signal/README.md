- 1. Features = the new columns you created (ma_5, price_vs_ma5, daily_returns) i.e Features are updated file data

- 2. Label = a future outcome column you have NOT created yet i.e "What happened AFTER today?”

```bash
Past ←──────── Today ────────→ Future
        ↑ features             ↑ label
```

- Features → what happened in the past

- Label → what we want to predict in the future

Example label:
```bash
Did the stock fall more than 3% in the next 5 days?
```

