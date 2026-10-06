const $ = (id) => document.getElementById(id);

function setValue(id, value) {
  $(id).textContent = value;
}

function cpuClass(value) {
  if (value < 50) return "good";
  if (value < 80) return "warning";
  return "critical";
}

async function updateSystem() {
  try {
    const response = await fetch("/api/system", { cache: "no-store" });
    if (!response.ok) throw new Error("System API failed");

    const data = await response.json();

    setValue("cpu", `${data.cpu}%`);
    setValue("ram", `${data.ram}%`);
    setValue("disk", `${data.disk}%`);
    setValue("uptime", data.uptime);
    setValue("ip", data.ip);
    setValue("upload", `${data.upload} MB/s`);
    setValue("download", `${data.download} MB/s`);
    setValue("latency", data.latency === null ? "Unavailable" : `${data.latency} ms`);

    $("cpu").className = cpuClass(data.cpu);

    labels.push(new Date().toLocaleTimeString());
    cpuValues.push(data.cpu);
    if (labels.length > 30) {
      labels.shift();
      cpuValues.shift();
    }
    cpuChart.update();

    $("health").textContent = "● Service healthy";
    $("health").className = "health healthy";
  } catch (error) {
    $("health").textContent = "● Service unavailable";
    $("health").className = "health unhealthy";
    console.error(error);
  }
}

async function updateWebsites() {
  try {
    const response = await fetch("/api/websites", { cache: "no-store" });
    if (!response.ok) throw new Error("Website API failed");

    const websites = await response.json();
    $("websites").innerHTML = websites.map(site => `
      <div class="website ${site.status === "Online" ? "online" : "offline"}">
        <strong>${site.name}</strong>
        <span>${site.status}</span>
        <small>${site.status_code ?? "N/A"} · ${site.latency}s</small>
      </div>
    `).join("");

    $("lastChecked").textContent = `Updated ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    console.error(error);
  }
}

async function updateDashboard() {
  await Promise.all([updateSystem(), updateWebsites()]);
}

updateDashboard();
setInterval(updateDashboard, 3000);
