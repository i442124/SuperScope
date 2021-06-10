const API_HOST = '192.168.1.1';
const API_PORT = '5000';

function onChooseFile(event, handler) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = handler;
    reader.readAsText(file);
}

function onFileRead(event, handler) {
    handler(event.target.result);
}

function onCaptureFrame(video, handler) {
    const canvas = document.createElement('canvas')
    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;

    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0);
    handler(canvas)
}

function find_recommendation(scores, game) {
    return scores.find(score => 
            score.title == game.title &&
            score.platform == game.platform)
}

function post(request, content=null, version=1.0){
    REQUEST_URL = `https://${API_HOST}:${API_PORT}/api/v${version}/${request}`;
    REQUEST_HEADERS = { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: content }
    return fetch(REQUEST_URL, REQUEST_HEADERS)
}