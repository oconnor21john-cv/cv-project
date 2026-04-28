/// <reference types="node" />
require("dotenv").config();
const express = require("express");

const app = express();

// Serve the pretty UI at http://localhost:3000/
app.use(express.static("z_api_food_test/public"));

function getApiKey(res: any) {
  const apiKey = process.env.SPOONACULAR_API_KEY;
  if (!apiKey) {
    res
      .status(500)
      .json({ error: "Missing SPOONACULAR_API_KEY (check your .env file)" });
    return null;
  }
  return apiKey;
}

app.get("/api/recipes", async (req: any, res: any) => {
  try {
    const apiKey = getApiKey(res);
    if (!apiKey) return;

    const q = String(req.query.q ?? "pasta");
    const offset = Math.max(0, Number(req.query.offset ?? 0) || 0);
    const number = Math.min(24, Math.max(1, Number(req.query.number ?? 12) || 12));

    const url = new URL("https://api.spoonacular.com/recipes/complexSearch");
    url.searchParams.set("query", q);
    url.searchParams.set("offset", String(offset));
    url.searchParams.set("number", String(number));
    url.searchParams.set("apiKey", apiKey);

    const r = await fetch(url);
    res.status(r.status).json(await r.json());
  } catch (err) {
    res.status(500).json({ error: "Request failed", details: String(err) });
  }
});

app.get("/api/recipes/:id", async (req: any, res: any) => {
  try {
    const apiKey = getApiKey(res);
    if (!apiKey) return;

    const id = Number(req.params.id);
    if (!Number.isFinite(id)) {
      return res.status(400).json({ error: "Invalid recipe id" });
    }

    const url = new URL(
      `https://api.spoonacular.com/recipes/${id}/information`
    );
    url.searchParams.set("includeNutrition", "false");
    url.searchParams.set("apiKey", apiKey);

    const r = await fetch(url);
    res.status(r.status).json(await r.json());
  } catch (err) {
    res.status(500).json({ error: "Request failed", details: String(err) });
  }
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});