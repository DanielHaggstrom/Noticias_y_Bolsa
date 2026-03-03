# Noticias y Bolsa

Archived academic project for predicting weekly S&P 500 movements from Financial Times news sentiment.

## Status

This repository was archived on March 3, 2026.

- Active development has stopped.
- The bundled Dash interface is kept in a deployable, read-only state.
- The research pipeline remains in the repository for reference, but it should be treated as historical code rather than an actively maintained product.

## What Is In The Repo

- `Interfaz/`: Dash application that serves bundled predictions and headline data.
- `datos/`: historical market data, scraped news, sentiment scores, and the training dataset used in the project.
- `FT.py`: legacy Financial Times scraping script.
- `analizar_noticias.py`: sentiment scoring step for scraped articles.
- `market_data.py`: Yahoo Finance weekly market data downloader.
- `generar_dataset_final.py`: dataset builder that joins market and sentiment data.
- `model.py`: legacy sequence-model training script.

## Quick Start

The supported path for this archived repository is the bundled dashboard.

1. Create an environment with Python 3.10 or newer.
2. Install the production dependencies:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the dashboard locally:

```powershell
python Interfaz\app.py
```

4. For a production-style Windows deployment, run it through Waitress:

```powershell
waitress-serve --listen=127.0.0.1:8050 Interfaz.app:server
```

## Legacy Research Environment

The original academic stack is preserved in `requirements-legacy-research.txt`.

- It is not part of the production deployment path.
- It is not guaranteed to reproduce the original training results on modern machines.
- The scraping code depends on external sites that have likely changed since the project was created.

## Notes On Historical Scripts

- `FT.py` no longer contains credentials. Set `FT_EMAIL` and `FT_PASSWORD` in the environment before running it.
- Financial Times scraping may require selector updates because the site structure has changed since the original work.
- `analizar_noticias.py` expects the NLTK VADER lexicon and will download it automatically if missing.

## Repository Cleanup

This archive intentionally excludes committed virtual environments, IDE metadata, and Python bytecode artifacts. Those files were removed from version control to keep the repository maintainable and portable.

## License

MIT License. See `LICENSE`.
