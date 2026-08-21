import React, { useEffect, useState } from "react";

function App() {
  const [projects, setProjects] = useState([]);
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch("/projects")
      .then((r) => r.json())
      .then((data) => setProjects(data))
      .catch(() => setProjects([]));

    fetch("/articles")
      .then((r) => r.json())
      .then((data) => setArticles(data))
      .catch(() => setArticles([]));
  }, []);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: 24 }}>
      <header>
        <h1>Phoenix Hub</h1>
        <nav>
          <a href="/">Home</a> {" | "}
          <a href="/admin">Admin</a> {" | "}
          <a href="/docs">API Docs</a>
        </nav>
      </header>

      <section style={{ marginTop: 24 }}>
        <h2>Projects</h2>
        {projects.length === 0 ? (
          <p>No projects available.</p>
        ) : (
          <ul>
            {projects.map((p, i) => (
              <li key={i}>
                <strong>{p.name}</strong> — {p.description} ({p.stack})
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Articles</h2>
        {articles.length === 0 ? (
          <p>No articles available.</p>
        ) : (
          <ul>
            {articles.map((a, i) => (
              <li key={i}>
                <strong>{a.title}</strong> — {a.category}
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer style={{ marginTop: 36, borderTop: "1px solid #eee", paddingTop: 12 }}>
        <small>© Phoenix Hub</small>
      </footer>
    </div>
  );
}

export default App;
