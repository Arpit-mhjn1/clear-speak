import sys

html = open('app.html', encoding='utf-8').read()

html = html.replace('maxNumHands: 1,', 'maxNumHands: 2,')
html = html.replace('let frameBuffer = [];', 'let frameBuffer = {};')

old_onresults_inner = """      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        
        drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: 'rgba(0, 229, 255, 0.8)', lineWidth: 4});
        drawLandmarks(canvasCtx, landmarks, {color: '#FFFFFF', lineWidth: 1, radius: 5});

        // Normalize landmarks
        const wrist = landmarks[0];
        const normalized = landmarks.map(lm => ({
            x: lm.x - wrist.x, 
            y: lm.y - wrist.y, 
            z: lm.z - wrist.z
        }));
        
        frameBuffer.push(normalized);
        if (frameBuffer.length > GESTURE_THRESHOLD / 2) {
            frameBuffer.shift(); 
        }

        let detectedGesture = null;

        if (Object.keys(islDictionary).length > 0 && frameBuffer.length === (GESTURE_THRESHOLD / 2)) {
            detectedGesture = matchDynamicGesture(frameBuffer, islDictionary);
        }
        if (!detectedGesture) {
            detectedGesture = recognizeStaticGesture(landmarks);
        }
        
        if (detectedGesture) {
          if (detectedGesture === currentGesture) {
            gestureFrames++;
            if (gestureFrames === GESTURE_THRESHOLD) {
              triggerAction(detectedGesture);
            }
          } else {
            currentGesture = detectedGesture;
            gestureFrames = 1;
          }
        } else {
          currentGesture = null;
          gestureFrames = 0;
        }
      } else {
        currentGesture = null;
        gestureFrames = 0;
        frameBuffer = []; 
      }"""

new_onresults_inner = """      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        let anyDetectedGesture = null;
        
        for (let i = 0; i < results.multiHandLandmarks.length; i++) {
          const landmarks = results.multiHandLandmarks[i];
          const handedness = results.multiHandedness ? results.multiHandedness[i].label : `hand_${i}`;
          
          if (!frameBuffer[handedness]) {
             frameBuffer[handedness] = [];
          }

          drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: 'rgba(0, 229, 255, 0.8)', lineWidth: 4});
          drawLandmarks(canvasCtx, landmarks, {color: '#FFFFFF', lineWidth: 1, radius: 5});

          // Normalize landmarks
          const wrist = landmarks[0];
          const normalized = landmarks.map(lm => ({
              x: lm.x - wrist.x, 
              y: lm.y - wrist.y, 
              z: lm.z - wrist.z
          }));
          
          frameBuffer[handedness].push(normalized);
          if (frameBuffer[handedness].length > GESTURE_THRESHOLD / 2) {
              frameBuffer[handedness].shift(); 
          }

          let detectedGesture = null;

          if (Object.keys(islDictionary).length > 0 && frameBuffer[handedness].length === (GESTURE_THRESHOLD / 2)) {
              detectedGesture = matchDynamicGesture(frameBuffer[handedness], islDictionary);
          }
          if (!detectedGesture) {
              detectedGesture = recognizeStaticGesture(landmarks);
          }
          
          if (detectedGesture) {
             anyDetectedGesture = detectedGesture;
          }
        }
        
        // Remove old hands that are no longer detected
        const currentLabels = results.multiHandedness ? results.multiHandedness.map(h => h.label) : results.multiHandLandmarks.map((_, i) => `hand_${i}`);
        for (const key of Object.keys(frameBuffer)) {
           if (!currentLabels.includes(key)) {
               frameBuffer[key] = [];
           }
        }

        if (anyDetectedGesture) {
          if (anyDetectedGesture === currentGesture) {
            gestureFrames++;
            if (gestureFrames === GESTURE_THRESHOLD) {
              triggerAction(anyDetectedGesture);
            }
          } else {
            currentGesture = anyDetectedGesture;
            gestureFrames = 1;
          }
        } else {
          currentGesture = null;
          gestureFrames = 0;
        }
      } else {
        currentGesture = null;
        gestureFrames = 0;
        frameBuffer = {}; 
      }"""

if old_onresults_inner in html:
    html = html.replace(old_onresults_inner, new_onresults_inner)
    open('app.html', 'w', encoding='utf-8').write(html)
    print("Successfully added dual-hand support.")
else:
    print("Could not find the old onResults inner block.")
