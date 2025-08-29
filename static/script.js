const statusEl = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");
const feedbackEl = document.getElementById("feedback");
const metricsEl = document.getElementById("metricsChart");
const waveformCanvas = document.getElementById("waveform");

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const exitBtn = document.getElementById("exitBtn");
const replayBtn = document.getElementById("replayBtn");

let lastHeckle = "";
let metricsChart;
let waveformAnimation;
let partialHeckleInterval;

let audioCtx, analyser, dataArray, source;

// --- Setup Chart.js ---
metricsChart = new Chart(metricsEl, {
    type: 'bar',
    data: {
        labels: ['Words', 'WPM', 'Filler Words', 'Sentiment'],
        datasets: [{
            label: 'Metrics',
            data: [0,0,0,0],
            backgroundColor: ['#1DB954', '#1ED760', '#1DB954', '#1ED760']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// --- Waveform functions ---
const waveformCtx = waveformCanvas.getContext('2d');

function stopWaveform(){
    cancelAnimationFrame(waveformAnimation);
    waveformCtx.clearRect(0,0,waveformCanvas.width,waveformCanvas.height);
    if(audioCtx){
        audioCtx.close();
        audioCtx = null;
    }
}

// Reactive waveform using microphone input
async function startWaveformReactive() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);

        analyser.fftSize = 256;
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);

        drawReactiveWaveform();
    } catch (err) {
        console.error("Error accessing microphone:", err);
    }
}

function drawReactiveWaveform() {
    const width = waveformCanvas.width;
    const height = waveformCanvas.height;
    waveformCtx.clearRect(0, 0, width, height);

    if(analyser){
        analyser.getByteTimeDomainData(dataArray);
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
            sum += (dataArray[i] - 128) * (dataArray[i] - 128);
        }
        const rms = Math.sqrt(sum / dataArray.length); // volume level

        // Only draw waveform if sound above threshold
        if (rms > 5) {
            for (let i = 0; i < width; i += 4) {
                let y = height / 2 + Math.sin(Date.now() / 200 + i / 5) * rms * 1.5;
                waveformCtx.fillStyle = '#1DB954';
                waveformCtx.fillRect(i, y, 3, 2);
            }
        }
    }

    waveformAnimation = requestAnimationFrame(drawReactiveWaveform);
}

// --- Start recording ---
startBtn.onclick = async () => {
    statusEl.textContent = "🎙 Recording... Speak now!";
    startBtn.disabled = true;
    stopBtn.disabled = false;

    startWaveformReactive(); // start reactive waveform

    // Start fetching partial heckles every 2 seconds
    partialHeckleInterval = setInterval(async () => {
        try {
            const res = await fetch('/get_partial_feedback');
            const data = await res.json();
            if (data.heckle) {
                feedbackEl.textContent += "\n" + data.heckle;
                lastHeckle = data.heckle;
                replayBtn.disabled = false;
            }
        } catch (e) {
            console.error("Partial feedback error:", e);
        }
    }, 2000);

    try {
        const res = await fetch("/start", { method: "POST" });
        const data = await res.json();
        if (data.error) throw new Error(data.error);
    } catch (e) {
        statusEl.textContent = "❌ Error starting recording.";
        startBtn.disabled = false;
        stopBtn.disabled = true;
        stopWaveform();
        clearInterval(partialHeckleInterval);
        console.error(e);
    }
};

// --- Stop recording ---
stopBtn.onclick = async () => {
    statusEl.textContent = "⏳ Processing...";
    stopBtn.disabled = true;
    stopWaveform();
    clearInterval(partialHeckleInterval);

    try {
        const res = await fetch("/stop", { method: "POST" });
        const data = await res.json();

        if (!data.feedback || data.feedback.trim() === "") {
            data.feedback = "🤡 I am forced to heckle you! Speak next time!";
        }

        transcriptEl.textContent = data.transcript || "(No clear speech detected)";
        feedbackEl.textContent += "\n" + data.feedback;
        lastHeckle = data.feedback;

        replayBtn.disabled = !lastHeckle;

        const m = data.metrics || {};
        metricsChart.data.datasets[0].data = [
            m.word_count ?? 0,
            m.wpm ?? 0,
            m.filler_words ?? 0,
            m.sentiment === 'positive' ? 1 : m.sentiment === 'negative' ? -1 : 0
        ];
        metricsChart.update();

        statusEl.textContent = "✅ Done!";
    } catch (e) {
        statusEl.textContent = "❌ Error processing!";
        console.error(e);
    } finally {
        startBtn.disabled = false;
    }
};

// --- Replay last heckle ---
replayBtn.onclick = async () => {
    if (!lastHeckle) return;
    try {
        await fetch("/replay");
    } catch (e) {
        console.error(e);
    }
};

// --- Exit ---
exitBtn.onclick = async () => {
    statusEl.textContent = "🚪 Exiting...";
    try {
        await fetch("/exit", { method: "POST" });
        setTimeout(() => window.close(), 500);
    } catch (e) {
        console.error(e);
    }
};
