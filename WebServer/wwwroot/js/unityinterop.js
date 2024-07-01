var myGameInstance = null;
var oldFocus = 2;

initViewUnity = function(width, height) {
  forbidBrowserGestures();
  var canvas = document.querySelector("#unity-canvas");
  var progressBarFull = document.querySelector("#unity-progress-bar-full");
  
  var buildUrl = "../UnityBuild/Build";
  var loaderUrl = buildUrl + "/WebGL.loader.js";
  var config = {
    dataUrl: buildUrl + "/WebGL.data",
    frameworkUrl: buildUrl + "/WebGL.framework.js",
    codeUrl: buildUrl + "/WebGL.wasm",
    streamingAssetsUrl: "../UnityBuild/StreamingAssets",
    companyName: "DefaultCompany",
    productName: "UnityRobot",
    productVersion: "0.1",
  };


  canvas.style.width = width + "px";
  canvas.style.height = height + "px";
 

  var script = document.createElement("script");
  script.src = loaderUrl;
  script.onload = () => {
    createUnityInstance(canvas, config, (progress) => {
      progressBarFull.style.width = 100 * progress + "%";
          }).then((unityInstance) => {
            myGameInstance = unityInstance;
          }).catch((message) => {
            alert(message);
          });
        };

  document.body.appendChild(script);

  document.addEventListener('click', function(e) {
    if (e.target.id == "unity-canvas") {
        // Clicked on canvas
        focusCanvas(1);
    } else {
        // Clicked outside of canvas
        focusCanvas(0);
    }
  });
}

registerEvent = function(dotNetObject) {
    const iframe = document.getElementById("unity-container");

    iframe.onload = function() {
        // 通过 postMessage 向 iframe 发送消息
        iframe.contentWindow.postMessage("Hello from parent", "*");
    };

    window.addEventListener("message", function(event) {
        dotNetObject.invokeMethodAsync("OnIframeEvent", event.data);
    });
}

/*
* 禁用浏览器手势
*/
function forbidBrowserGestures() {
  var isEdge = /Edg/.test(navigator.userAgent);
  var isMobile = /Mobi|Android/i.test(navigator.userAgent);
  if(isEdge && !isMobile) {
    document.addEventListener('wheel', function(e) {
      if(e.ctrlKey) {
        e.preventDefault();
      }
    }, {passive: false});
  }
  if (isEdge) {
    document.addEventListener("MSPointerMove", function(e) {
      if (e.pointerType === "mouse" && e.getIntermediatePoints().length > 1) {
        e.preventDefault();
      }
    }, {passive: false});
  }
}

/*
* 键盘事件处理函数
*/
var thisDotNetObject = null;
function onKeyDown(event) {
  thisDotNetObject.invokeMethodAsync("OnKeyDown", event.key);
}

function onKeyUp(event) {
  thisDotNetObject.invokeMethodAsync("OnKeyUp", event.key);
}

registerKeyEvent = function(dotNetObject) {
  thisDotNetObject = dotNetObject;
  window.addEventListener("keydown", onKeyDown);
  window.addEventListener("keyup", onKeyUp);
}

unregisterKeyEvent = function()
{
  window.removeEventListener("keydown", onKeyDown);
  window.removeEventListener("keyup", onKeyUp);
}

/**
 * 弹窗函数
 */
showConfirmation = function(message) {
  return confirm(message);
}

/**
 * Unity键盘控制函数
 */
focusCanvas = function(focus) {
  if(oldFocus == focus)
  {
    return;
  }
  oldFocus = focus;
  myGameInstance.SendMessage('GameMaster','JSFocusCanvas',focus);
}

/**
 * 获取窗口尺寸
 */
getWindowSize = function() {
  return [window.innerWidth, window.innerHeight];
}