import React, { useEffect, useMemo, useState } from "react";

const getCurrentView = () => (window.location.pathname.startsWith("/admin") ? "admin" : "home");

function App() {
  const [currentView, setCurrentView] = useState(getCurrentView());
  const [projects, setProjects] = useState([]);
  const [articles, setArticles] = useState([]);
  const [education, setEducation] = useState([]);
  const [summary, setSummary] = useState({ projects: 0, articles: 0, status: "ok" });
  const [token, setToken] = useState(() => localStorage.getItem("phoenix-admin-token") || "");
  const [loginForm, setLoginForm] = useState({ username: "admin", password: "" });
  const [profileForm, setProfileForm] = useState({ name: "Phoenix Hub", mission: "Engineering platform" });
  const [articleForm, setArticleForm] = useState({ title: "", slug: "", category: "Engineering", content: "" });
  const [status, setStatus] = useState("Ready");
  const [profileMessage, setProfileMessage] = useState("");

  const adminReady = useMemo(() => Boolean(token), [token]);

  useEffect(() => {
    const onPopState = () => setCurrentView(getCurrentView());
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, []);

  const loadAdminData = async () => {
    try {
      const [projectsResponse, articlesResponse, educationResponse, summaryResponse, profileResponse] = await Promise.all([
        fetch("/projects"),
        fetch("/articles"),
        fetch("/education"),
        fetch("/admin/summary"),
        token ? fetch("/admin/profile", { headers: { Authorization: `Bearer ${token}` } }) : Promise.resolve(null),
      ]);

      const nextProjects = projectsResponse ? await projectsResponse.json() : [];
      const nextArticles = articlesResponse ? await articlesResponse.json() : [];
      const nextEducation = educationResponse ? await educationResponse.json() : [];
      const nextSummary = summaryResponse ? await summaryResponse.json() : { projects: 0, articles: 0, status: "ok" };

      setProjects(nextProjects);
      setArticles(nextArticles);
      setEducation(nextEducation);
      setSummary(nextSummary);

      if (profileResponse && profileResponse.ok) {
        const nextProfile = await profileResponse.json();
        setProfileForm({ name: nextProfile.name || profileForm.name, mission: nextProfile.mission || profileForm.mission });
      } else if (profileResponse && profileResponse.status === 401) {
        setToken("");
        localStorage.removeItem("phoenix-admin-token");
        setStatus("Your session has expired. Please sign in again.");
      }
    } catch (error) {
      setProjects([]);
      setArticles([]);
      setEducation([]);
      setSummary({ projects: 0, articles: 0, status: "ok" });
    }
  };

  useEffect(() => {
    loadAdminData();
  }, [token]);

  const handleNavigate = (path) => {
    window.history.pushState({}, "", path);
    setCurrentView(getCurrentView());
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    setStatus("Authenticating...");

    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginForm),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Authentication failed");
      }

      setToken(payload.token);
      localStorage.setItem("phoenix-admin-token", payload.token);
      setStatus("Authenticated");
      setProfileMessage("Logged in successfully.");
    } catch (error) {
      setStatus(error.message || "Login failed");
      setProfileMessage(error.message || "Login failed");
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("phoenix-admin-token");
    setStatus("Logged out");
    setProfileMessage("Logged out.");
  };

  const handleDeleteArticle = async (slug) => {
    try {
      const response = await fetch(`/admin/articles/${slug}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        throw new Error("Unable to delete article");
      }

      setStatus("Article deleted");
      setProfileMessage(`Deleted article: ${slug}`);
      loadAdminData();
    } catch (error) {
      setStatus(error.message || "Delete failed");
      setProfileMessage(error.message || "Delete failed");
    }
  };

  const handleProfileSave = async (event) => {
    event.preventDefault();
    setStatus("Saving profile...");

    try {
      const response = await fetch("/admin/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(profileForm),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to update profile");
      }

      setStatus("Profile updated");
      setProfileMessage("Profile updated successfully.");
    } catch (error) {
      setStatus(error.message || "Profile update failed");
      setProfileMessage(error.message || "Profile update failed");
    }
  };

  const handleArticleSubmit = async (event) => {
    event.preventDefault();
    setStatus("Publishing article...");

    try {
      const response = await fetch("/admin/articles", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(articleForm),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to create article");
      }

      setStatus("Article published");
      setArticleForm({ title: "", slug: "", category: "Engineering", content: "" });
      setProfileMessage(`Article created: ${payload.title}`);
      fetch("/articles")
        .then((r) => r.json())
        .then((data) => setArticles(data))
        .catch(() => setArticles([]));
    } catch (error) {
      setStatus(error.message || "Article creation failed");
      setProfileMessage(error.message || "Article creation failed");
    }
  };

  const styles = {
    page: { fontFamily: "system-ui, sans-serif", background: "#0b1020", color: "#e5ecff", minHeight: "100vh", padding: 24 },
    shell: { maxWidth: 1200, margin: "0 auto" },
    topbar: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 32 },
    nav: { display: "flex", gap: 12, flexWrap: "wrap" },
    link: { color: "#8bb4ff", textDecoration: "none", cursor: "pointer" },
    section: { background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 16, padding: 20, marginBottom: 20 },
    grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16 },
    card: { background: "rgba(139,180,255,0.05)", borderRadius: 12, padding: 18, border: "1px solid rgba(139,180,255,0.12)" },
    button: { background: "#7c9cff", color: "#081120", border: "none", borderRadius: 10, padding: "10px 16px", cursor: "pointer", fontWeight: 700 },
    secondaryButton: { background: "transparent", color: "#dfe8ff", border: "1px solid rgba(255,255,255,0.15)", borderRadius: 10, padding: "10px 16px", cursor: "pointer" },
    form: { display: "grid", gap: 12 },
    input: { background: "#111827", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8, color: "#e5ecff", padding: 10 },
    textarea: { background: "#111827", border: "1px solid rgba(255,255,255,0.12)", borderRadius: 8, color: "#e5ecff", padding: 10, minHeight: 120 },
    list: { margin: 0, paddingLeft: 20, color: "#dfe8ff" },
    badge: { display: "inline-block", padding: "6px 10px", borderRadius: 999, background: "rgba(84,211,154,0.12)", color: "#7ef0b8", fontSize: 12, fontWeight: 700 },
  };

  if (currentView === "admin") {
    return (
      <div style={styles.page}>
        <div style={styles.shell}>
          <header style={styles.topbar}>
            <div>
              <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: "uppercase", color: "#7db0ff" }}>Phoenix Hub</div>
              <h1 style={{ margin: "8px 0 0" }}>Admin Panel</h1>
            </div>
            <nav style={styles.nav}>
              <span style={styles.link} onClick={() => handleNavigate("/")}>Home</span>
              <span style={styles.link} onClick={() => handleNavigate("/admin")}>Admin</span>
            </nav>
          </header>

          <section style={styles.section}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
              <span style={styles.badge}>{status}</span>
              {adminReady && <button style={styles.secondaryButton} onClick={handleLogout}>Logout</button>}
            </div>
          </section>

          {!adminReady ? (
            <section style={styles.section}>
              <h2>Login</h2>
              <p>Use the administrator credentials configured in Render.</p>
              <form onSubmit={handleLogin} style={styles.form}>
                <input aria-label="Username" autoComplete="username" required style={styles.input} value={loginForm.username} onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })} placeholder="Username" />
                <input aria-label="Password" autoComplete="current-password" required type="password" style={styles.input} value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder="Password" />
                <button style={styles.button} type="submit">Sign in</button>
              </form>
              {profileMessage && <p style={{ color: "#ffd8a8" }}>{profileMessage}</p>}
            </section>
          ) : (
            <>
              <section style={styles.grid}>
                <div style={styles.card}>
                  <div style={{ color: "#8bb4ff", fontSize: 12, textTransform: "uppercase" }}>Projects</div>
                  <h3 style={{ margin: "12px 0 0", fontSize: 32 }}>{summary.projects || projects.length}</h3>
                </div>
                <div style={styles.card}>
                  <div style={{ color: "#8bb4ff", fontSize: 12, textTransform: "uppercase" }}>Articles</div>
                  <h3 style={{ margin: "12px 0 0", fontSize: 32 }}>{summary.articles || articles.length}</h3>
                </div>
                <div style={styles.card}>
                  <div style={{ color: "#8bb4ff", fontSize: 12, textTransform: "uppercase" }}>Status</div>
                  <h3 style={{ margin: "12px 0 0", fontSize: 14 }}>{summary.status}</h3>
                </div>
              </section>

              <section style={styles.section}>
                <h2>Profile</h2>
                <form style={styles.form} onSubmit={handleProfileSave}>
                  <input style={styles.input} value={profileForm.name} onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })} placeholder="Name" />
                  <input style={styles.input} value={profileForm.mission} onChange={(e) => setProfileForm({ ...profileForm, mission: e.target.value })} placeholder="Mission" />
                  <button style={styles.button} type="submit">Update profile</button>
                </form>
              </section>

              <section style={styles.section}>
                <h2>New article</h2>
                <form style={styles.form} onSubmit={handleArticleSubmit}>
                  <input style={styles.input} value={articleForm.title} onChange={(e) => setArticleForm({ ...articleForm, title: e.target.value })} placeholder="Title" />
                  <input style={styles.input} value={articleForm.slug} onChange={(e) => setArticleForm({ ...articleForm, slug: e.target.value })} placeholder="Slug" />
                  <input style={styles.input} value={articleForm.category} onChange={(e) => setArticleForm({ ...articleForm, category: e.target.value })} placeholder="Category" />
                  <textarea style={styles.textarea} value={articleForm.content} onChange={(e) => setArticleForm({ ...articleForm, content: e.target.value })} placeholder="Content" />
                  <button style={styles.button} type="submit">Publish article</button>
                </form>
              </section>

              <section style={styles.section}>
                <h2>Published articles</h2>
                <div style={{ display: "grid", gap: 12 }}>
                  {articles.length === 0 ? (
                    <p>No articles available.</p>
                  ) : (
                    articles.map((article) => (
                      <div key={article.slug} style={{ ...styles.card, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, flexWrap: "wrap" }}>
                        <div>
                          <strong>{article.title}</strong>
                          <div style={{ color: "#a9bbd6", fontSize: 12 }}>{article.category}</div>
                        </div>
                        <button style={styles.secondaryButton} onClick={() => handleDeleteArticle(article.slug)}>Delete</button>
                      </div>
                    ))
                  )}
                </div>
              </section>

              {profileMessage && <section style={styles.section}><p>{profileMessage}</p></section>}
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <div style={styles.shell}>
        <header style={styles.topbar}>
          <div>
            <div style={{ fontSize: 12, letterSpacing: 1.2, textTransform: "uppercase", color: "#7db0ff" }}>Engineering</div>
            <h1 style={{ margin: "8px 0 0" }}>Phoenix Hub</h1>
          </div>
        </header>

        <section style={styles.section}>
          <h2>Professional platform and engineering lab</h2>
          <p>Cloud, DevOps, automation, platform engineering and technical innovation.</p>
        </section>

        <section style={styles.grid}>
          <div style={styles.card}>
            <h3>Projects</h3>
            <ul style={styles.list}>
              {projects.length === 0 ? <li>No projects available.</li> : projects.map((project) => <li key={project.name}>{project.name}</li>)}
            </ul>
          </div>

          <div style={styles.card}>
            <h3>Articles</h3>
            <ul style={styles.list}>
              {articles.length === 0 ? <li>No articles available.</li> : articles.map((article) => <li key={article.slug}>{article.title}</li>)}
            </ul>
          </div>
        </section>

        <section style={styles.section}>
          <h2>Professional Education</h2>
          {education.length === 0 ? (
            <p>No education information available.</p>
          ) : (
            <div style={styles.grid}>
              {education.map((item) => (
                <div key={`${item.institution}-${item.degree}`} style={styles.card}>
                  <h3 style={{ marginTop: 0 }}>{item.degree}</h3>
                  <p style={{ margin: "0 0 6px" }}>{item.institution}</p>
                  <div style={{ color: "#a9bbd6", fontSize: 14 }}>{item.period}</div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;
