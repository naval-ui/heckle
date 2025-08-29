const statusEl = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");
const feedbackEl = document.getElementById("feedback");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const exitBtn = document.getElementById("exitBtn");
const metricsEl = document.getElementById("metrics");

startBtn.onclick = async () => {
  statusEl.textContent = "🎙 Recording... Speak now!";
  startBtn.disabled = true;
  stopBtn.disabled = false;

  try {
    const res = await fetch("/start", { method: "POST" });
    const data = await res.json();
    if (data.error) throw new Error(data.error);
  } catch (e) {
    statusEl.textContent = "❌ Error starting recording.";
    startBtn.disabled = false;
    stopBtn.disabled = true;
    console.error(e);
  }
};

stopBtn.onclick = async () => {
  statusEl.textContent = "⏳ Processing...";
  stopBtn.disabled = true;

  try {
    const res = await fetch("/stop", { method: "POST" });
    const data = await res.json();

    if (data.error) {
      statusEl.textContent = "❌ Error processing!";
      console.error(data.error);
      return;
    }

    transcriptEl.textContent = data.transcript && data.transcript.trim() !== "" ? data.transcript : "(No clear speech detected)";
    feedbackEl.textContent = data.feedback || "—";

    // Show metrics
    const m = data.metrics || {};
    metricsEl.innerHTML = `
      <div><b>Words:</b> ${m.word_count ?? "-"}</div>
      <div><b>WPM:</b> ${m.wpm ?? "-"}</div>
      <div><b>Filler words:</b> ${m.filler_words ?? "-"}</div>
      <div><b>Sentiment:</b> ${m.sentiment ?? "-"}</div>
    `;

    statusEl.textContent = "✅ Done!";
  } catch (e) {
    statusEl.textContent = "❌ Error processing!";
    console.error(e);
  } finally {
    startBtn.disabled = false;
  }
};

exitBtn.onclick = async () => {
  statusEl.textContent = "🚪 Exiting...";
  try {
    await fetch("/exit", { method: "POST" });
    // Small delay so TTS can finish
    setTimeout(() => window.close(), 500);
  } catch (e) {
    console.error(e);
  }
};
