import { useEffect, useRef } from 'react';

const GraphCanvas = ({ nodes, edges }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const parent = canvas.parentElement;

    // Set canvas size to match parent
    const resizeCanvas = () => {
      canvas.width = parent.clientWidth;
      canvas.height = parent.clientHeight;
    };

    // Initial size
    resizeCanvas();

    // Add resize listener
    window.addEventListener('resize', resizeCanvas);

    // Draw nodes and edges
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Calculate node positions (simple grid layout for now)
      const nodePositions = nodes.map((node, i) => ({
        x: 100 + (i % 3) * 200,
        y: 100 + Math.floor(i / 3) * 200,
        node
      }));

      // Draw edges
      edges.forEach(edge => {
        const source = nodePositions.find(pos => pos.node.id === edge.source);
        const target = nodePositions.find(pos => pos.node.id === edge.target);

        if (source && target) {
          ctx.beginPath();
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
          ctx.strokeStyle = '#666';
          ctx.stroke();

          // Draw relationship text
          const midX = (source.x + target.x) / 2;
          const midY = (source.y + target.y) / 2;
          ctx.fillStyle = '#333';
          ctx.font = '12px sans-serif';
          ctx.fillText(edge.relationship, midX, midY);
        }
      });

      // Draw nodes
      nodePositions.forEach(({ x, y, node }) => {
        ctx.beginPath();
        ctx.arc(x, y, 30, 0, 2 * Math.PI);
        ctx.fillStyle = getNodeColor(node.type);
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.stroke();

        // Draw node text
        ctx.fillStyle = '#333';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(node.type, x, y);
      });
    };

    // Color mapping for node types
    const getNodeColor = (type) => {
      const colors = {
        Role: '#90cdf4',    // blue
        Achievement: '#9ae6b4', // green
        Skill: '#fbd38d'     // yellow
      };
      return colors[type] || '#cbd5e0';
    };

    // Draw initially and on updates
    draw();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
    };
  }, [nodes, edges]);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
    />
  );
};

export default GraphCanvas;