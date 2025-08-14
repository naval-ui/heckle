document.getElementById("startBtn").onclick = async () => {
    const statusEl = document.getElementById("status");
    const transcriptEl = document.getElementById("transcript");
    const heckleEl = document.getElementById("heckle");

    statusEl.textContent = "🎙 Recording... Speak now!";
    statusEl.style.backgroundColor = "rgba(255, 153, 0, 0.58)";
    document.getElementById("startBtn").disabled = true;
    document.getElementById("stopBtn").disabled = false;

    try {
        const res = await fetch("/start", { method: "POST" });
        const data = await res.json();
        if (data.error) {
            statusEl.textContent = "❌ Error starting recording!";
            statusEl.style.backgroundColor = "rgba(199, 50, 40, 0.3)";
            console.error(data.error);
        }
    } catch (err) {
        console.error("Error:", err);
        statusEl.textContent = "❌ Error starting recording!";
        statusEl.style.backgroundColor = "rgba(199, 50, 40, 0.3)";
    }
};

document.getElementById("stopBtn").onclick = async () => {
    const statusEl = document.getElementById("status");
    const transcriptEl = document.getElementById("transcript");
    const heckleEl = document.getElementById("heckle");

    statusEl.textContent = "⏳ Processing...";
    statusEl.style.backgroundColor = "rgba(255, 235, 59, 0.3)";
    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;

    try {
        const res = await fetch("/stop", { method: "POST" });
        const data = await res.json();

        console.log('Recording stopped:', data);

        // Force heckle to "Coward!"
        heckleEl.innerText = "Coward!";

        if (data.error) {
            statusEl.textContent = "❌ Error processing!";
            statusEl.style.backgroundColor = "rgba(199, 50, 40, 0.3)";
            console.error(data.error);
        } else {
            transcriptEl.textContent = data.transcript || "(Silent)";
            statusEl.textContent = "✅ Done!";
            statusEl.style.backgroundColor = "rgba(76, 175, 80, 0.3)";
        }
    } catch (err) {
        console.error("Error:", err);
        statusEl.textContent = "❌ Error processing!";
        statusEl.style.backgroundColor = "rgba(199, 50, 40, 0.3)";
    }
};

document.getElementById("replayBtn").onclick = () => {
    const statusEl = document.getElementById("status");
    statusEl.textContent = "🔁 Replaying last heckle...";
    statusEl.style.backgroundColor = "rgba(10, 112, 159, 0.68)";

    fetch("/replay").then(() => {
        statusEl.textContent = "✅ Done!";
        statusEl.style.backgroundColor = "rgba(33, 221, 39, 0.83)";
    });
};

document.getElementById("resetBtn").onclick = () => {
    const statusEl = document.getElementById("status");
    const transcriptEl = document.getElementById("transcript");
    const heckleEl = document.getElementById("heckle");

    statusEl.textContent = "🔄 Resetting...";
    statusEl.style.backgroundColor = "rgba(255, 235, 59, 0.3)";
    transcriptEl.textContent = "";
    heckleEl.textContent = "";

    fetch("/reset").then(() => {
        statusEl.textContent = "✅ Reset!";
        statusEl.style.backgroundColor = "rgba(33, 221, 39, 0.83)";
        document.getElementById("startBtn").disabled = false;
        document.getElementById("stopBtn").disabled = true;
    });
};
