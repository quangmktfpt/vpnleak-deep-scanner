document.getElementById("ua").innerText = navigator.userAgent;
document.getElementById("timezone").innerText = Intl.DateTimeFormat().resolvedOptions().timeZone;

const rtc = new RTCPeerConnection({iceServers:[]});
rtc.createDataChannel("");
rtc.createOffer().then(o => rtc.setLocalDescription(o));
rtc.onicecandidate = e => {
    if (e && e.candidate) {
        const ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(e.candidate.candidate);
        if (ip) {
            document.getElementById("webrtc-leak").innerText = ip[1];
            document.getElementById("webrtc-leak").className = "fail";
        }
    } else {
        document.getElementById("webrtc-leak").innerText = "Không phát hiện";
        document.getElementById("webrtc-leak").className = "ok";
    }
};

function getCanvasFingerprint() {
    let canvas = document.createElement("canvas");
    let ctx = canvas.getContext("2d");
    ctx.textBaseline = "top";
    ctx.font = "16px Arial";
    ctx.fillText("VPN Leak Test", 2, 2);
    const fp = canvas.toDataURL();
    document.getElementById("canvas-fp").innerText = fp.substring(0, 50) + "...";
    document.getElementById("canvas-fp").className = "ok";
}
getCanvasFingerprint();

fetch("https://cloudflare-dns.com/dns-query?name=google.com&type=A", {
    method: "GET",
    headers: {
        "accept": "application/dns-json"
    }
}).then(r => r.json()).then(data => {
    const ip = data.Answer?.[0]?.data;
    if (ip) {
        document.getElementById("dns-leak").innerText = ip;
        document.getElementById("dns-leak").className = "fail";
    } else {
        document.getElementById("dns-leak").innerText = "Không phát hiện";
        document.getElementById("dns-leak").className = "ok";
    }
});
