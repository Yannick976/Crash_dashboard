### Ajouter une page

1. Créer `src/pages/ma_page.py` avec une fonction `layout(df)`
2. Importer dans `main.py` : `from src.pages import ma_page`
3. Ajouter la route dans le callback `display_page`
4. Ajouter le lien dans la navbar

### Ajouter un graphique

1. Dans la page concernée, créer une figure avec `plotly.express`
2. L'encapsuler dans un `dcc.Graph(figure=fig)`
3. Si interactif, ajouter un `@callback` avec `Input` et `Output`

### Lancer les tests

```bash
pip install pytest
pytest tests/
```

---

## Rapport d'analyse

- **~54 000 accidents** recensés en France métropolitaine en 2024
- Les mois de **juin, juillet et septembre** concentrent le plus d'accidents
- Les **routes départementales** sont les plus accidentogènes
- Les accidents par **temps normal** sont les plus fréquents, mais les conditions de **brouillard** et de **pluie forte** augmentent la gravité
- La majorité des accidents impliquent des **blessés légers**, mais on dénombre plusieurs milliers de **tués**

---

## Copyright

Je déclare sur l'honneur que le code fourni a été produit par moi-même, à l'exception des lignes ci-dessous :

| Fichier | Lignes | Source | Explication |
|---|---|---|---|
| `src/utils/clean_data.py` | `pd.to_numeric(..., errors="coerce")` | Documentation pandas | Conversion sécurisée en numérique |
| `src/pages/carte.py` | `px.scatter_mapbox(...)` | Documentation Plotly Express | Carte avec points géolocalisés |
| `main.py` | `dcc.Location` + callback routing | Documentation Dash | Navigation multi-pages Dash |