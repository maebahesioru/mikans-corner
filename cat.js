/* Mikan: a tiny pixel-ish cat drawn with plain canvas rects & paths.
   Reused across all three pages. No images, everything procedural. */
function drawMikan(canvas, opts = {}) {
  const X = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const pose = opts.pose || 'sit';
  const O = '#f7a354', D = '#de7c3c', C = '#ffe7c4', K = '#3d2b26', P = '#f7a8a8';
  X.clearRect(0, 0, W, H);
  X.save();
  X.translate(W / 2, H - 30);

  const s = 2.1; // scale factor
  const R = (x, y, w, h, col) => { X.fillStyle = col; X.fillRect(x * s, y * s, w * s, h * s); };

  // shadow
  X.fillStyle = 'rgba(0,0,0,.25)';
  X.beginPath();
  X.ellipse(0, 6, 46 * s / 2.1, 8 * s / 2.1, 0, 0, 7);
  X.fill();

  if (pose === 'sleep') {
    // curled loaf: a rounded blob with a tucked tail and closed eyes
    R(-30, -22, 60, 28, O);
    R(-26, -26, 20, 12, O);        // head bump
    R(-30, -30, 7, 8, O);          // ear
    R(-18, -30, 7, 8, O);          // ear
    R(-36, -18, 10, 10, D);        // tail curl
    R(-26, -13, 7, 3, K);          // closed eye 1
    R(-12, -13, 7, 3, K);          // closed eye 2
    R(-20, -8, 8, 4, C);           // muzzle
    X.fillStyle = '#8b93a8';
    X.font = '600 20px system-ui';
    X.fillText('z', 40, -40);
    X.font = '600 13px system-ui';
    X.fillText('z', 56, -58);
    X.restore();
    return;
  }

  if (pose === 'walk') {
    // body leaning, legs mid-stride
    R(-16, -34, 36, 26, O);
    R(-20, -46, 44, 36, O);        // head+body
    R(-24, -52, 12, 10, O);        // ears
    R(16, -52, 12, 10, O);
    R(-22, -50, 8, 6, P);
    R(18, -50, 8, 6, P);
    R(-9, -30, 7, 5, K);           // eyes
    R(5, -30, 7, 5, K);
    R(0, -23, 4, 3, P);            // nose
    R(-16, -8, 9, 14, O);          // front leg fwd
    R(4, -8, 9, 14, O);            // front leg
    R(10, -6, 12, 8, O);           // back paw
    R(-12, -44, 4, 5, D);          // stripes
    R(6, -44, 4, 5, D);
    if (opts.wag) R(24, -30, 10, 6, O); else R(26, -22, 10, 6, O);
    X.restore();
    return;
  }

  // default: sitting pose
  R(-16, -34, 32, 26, C);          // chest (ends above the feet)
  R(-20, -36, 40, 30, O);          // body top... keep simple full body
  R(-20, -58, 40, 34, O);          // head block
  R(-29, -63, 13, 11, O);          // ears (bigger)
  R(16, -63, 13, 11, O);
  R(-25, -60, 7, 7, P);            // inner ears
  R(18, -60, 7, 7, P);
  R(-11, -46, 8, 6, K);            // eyes
  R(3, -46, 8, 6, K);
  R(-2, -38, 5, 4, P);             // nose
  R(-8, -32, 16, 8, C);            // muzzle
  R(-4, -31, 3, 2, K);             // tiny mouth
  R(1, -31, 3, 2, K);
  R(-29, -30, 9, 1, '#e8dcc8');    // whiskers (symmetric)
  R(-29, -26, 9, 1, '#e8dcc8');
  R(20, -30, 9, 1, '#e8dcc8');
  R(20, -26, 9, 1, '#e8dcc8');
  R(-16, -56, 5, 5, D);            // forehead stripes (inside the head now)
  R(-2, -57, 4, 6, D);
  R(11, -56, 5, 5, D);
  R(-14, -2, 11, 10, O);           // feet
  R(3, -2, 11, 10, O);
  // tail (with optional wag)
  X.beginPath();
  X.strokeStyle = O;
  X.lineWidth = 8 * s / 2.1;
  X.lineCap = 'round';
  const wag = opts.wag ? 6 : 0;
  X.moveTo(20 * s / 2.1, -8 * s / 2.1);
  X.quadraticCurveTo((36 + wag) * s / 2.1, -16 * s / 2.1, (32 + wag * 1.4) * s / 2.1, -38 * s / 2.1);
  X.stroke();

  if (opts.star) {
    // a little star she's holding/caught
    X.fillStyle = '#f7c948';
    X.beginPath();
    const cx = 30, cy = -30, spikes = 5, outer = 13, inner = 6;
    for (let i = 0; i < spikes * 2; i++) {
      const r = i % 2 === 0 ? outer : inner;
      const a = (Math.PI / spikes) * i - Math.PI / 2;
      X[i === 0 ? 'moveTo' : 'lineTo'](cx + Math.cos(a) * r, cy + Math.sin(a) * r);
    }
    X.closePath();
    X.fill();
  }
  if (opts.mikan) {
    // a round mandarin orange snack
    X.fillStyle = '#f28c28';
    X.beginPath();
    X.arc(34, -16, 14, 0, 7);
    X.fill();
    X.fillStyle = '#5f9b3a';
    X.beginPath();
    X.ellipse(38, -30, 7, 4, -0.6, 0, 7);
    X.fill();
  }
  if (opts.heart) {
    X.fillStyle = '#f77';
    X.font = '22px serif';
    X.fillText('♥', 52, -70);
  }
  if (opts.blush) {
    X.fillStyle = 'rgba(247,168,168,.5)';
    X.beginPath();
    X.arc(-16 * s / 2.1 - 22, -40 * s / 2.1, 7, 0, 7);
    X.arc(16 * s / 2.1 + 22, -40 * s / 2.1, 7, 0, 7);
    X.fill();
  }
  if (opts.hearts) {
    X.fillStyle = '#f77';
    X.font = '18px serif';
    const hh = [[-60, -80], [-40, -100], [40, -90], [58, -76], [8, -110]];
    for (const [hx, hy] of hh) X.fillText('♥', hx, hy);
  }
  X.restore();
}
