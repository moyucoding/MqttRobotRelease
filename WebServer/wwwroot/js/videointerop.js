
// https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8
loadVideo = function(element, src) {
    var video = document.getElementById(element);
    var videoSrc = src;
    if (Hls.isSupported()) {
    var hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
    video.style.display = 'block';

    }
}

closeVideo = function(element) {
    var video = document.getElementById(element);
    if (video) {
        // 暂停视频播放
        video.pause();
        
        // 如果使用了Hls.js，你可能需要停止Hls.js的加载和播放
        if (Hls.isSupported()) {
            var hls = new Hls();
            hls.destroy();
        }
        
        // 隐藏视频元素（可选）
        video.style.display = 'none';
    }
}