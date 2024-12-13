import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Link2 } from 'lucide-react';
import GraphCanvas from './GraphCanvas';

const GraphBuilder = () => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [showNodeForm, setShowNodeForm] = useState(false);
  const [showEdgeForm, setShowEdgeForm] = useState(false);
  const [currentNode, setCurrentNode] = useState({
    type: 'Role',
    properties: {}
  });

  const nodeTypes = {
    Role: {
      properties: {
        level: ['Company', 'Department', 'Job'],
        startDate: 'date',
        endDate: 'date'
      }
    },
    Achievement: {
      properties: {
        type: ['Award', 'Accomplishment'],
        date: 'date',
        endDate: 'date'
      }
    },
    Skill: {
      properties: {
        type: ['Soft', 'Technical'],
        timesUsed: 'number',
        yearsExperience: 'number'
      }
    }
  };

  const handleNodeSubmit = (e) => {
    e.preventDefault();
    const newNode = { ...currentNode, id: nodes.length };
    setNodes([...nodes, newNode]);
    setShowNodeForm(false);
    setCurrentNode({ type: 'Role', properties: {} });
  };

  const handleEdgeSubmit = (e) => {
    e.preventDefault();
    if (selectedNodes.length === 2) {
      const newEdge = {
        source: selectedNodes[0],
        target: selectedNodes[1],
        relationship: document.getElementById('relationship').value,
        id: edges.length
      };
      setEdges([...edges, newEdge]);
      setSelectedNodes([]);
      setShowEdgeForm(false);
    }
  };

  const handleNodeSelect = (nodeId) => {
    if (selectedNodes.includes(nodeId)) {
      setSelectedNodes(selectedNodes.filter(id => id !== nodeId));
    } else if (selectedNodes.length < 2) {
      setSelectedNodes([...selectedNodes, nodeId]);
    }
  };

  return (
    <div className="h-screen w-screen flex">
      {/* Left sidebar for controls */}
      <div className="w-96 border-r p-4 flex flex-col">
        <div className="mb-4">
          <h1 className="text-2xl font-bold mb-4">Knowledge Graph Builder</h1>
          <div className="space-y-2">
            <Button 
              onClick={() => setShowNodeForm(true)}
              className="w-full bg-blue-500 hover:bg-blue-600"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Node
            </Button>
            <Button
              onClick={() => setShowEdgeForm(true)}
              disabled={selectedNodes.length !== 2}
              className="w-full bg-green-500 hover:bg-green-600"
            >
              <Link2 className="w-4 h-4 mr-2" />
              Add Edge
            </Button>
          </div>
        </div>

        {/* Forms */}
        {showNodeForm && (
          <Card className="mb-4">
            <CardHeader>
              <CardTitle>Add New Node</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleNodeSubmit} className="space-y-4">
                <div>
                  <label className="block mb-2">Type</label>
                  <select 
                    value={currentNode.type}
                    onChange={(e) => setCurrentNode({ type: e.target.value, properties: {} })}
                    className="w-full p-2 border rounded"
                  >
                    {Object.keys(nodeTypes).map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>

                {Object.entries(nodeTypes[currentNode.type].properties).map(([prop, type]) => (
                  <div key={prop}>
                    <label className="block mb-2 capitalize">{prop}</label>
                    {Array.isArray(type) ? (
                      <select 
                        onChange={(e) => setCurrentNode({
                          ...currentNode,
                          properties: { ...currentNode.properties, [prop]: e.target.value }
                        })}
                        className="w-full p-2 border rounded"
                      >
                        <option value="">Select {prop}</option>
                        {type.map(option => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </select>
                    ) : (
                      <input 
                        type={type}
                        onChange={(e) => setCurrentNode({
                          ...currentNode,
                          properties: { ...currentNode.properties, [prop]: e.target.value }
                        })}
                        className="w-full p-2 border rounded"
                      />
                    )}
                  </div>
                ))}

                <Button type="submit" className="w-full bg-blue-500 hover:bg-blue-600">
                  Create Node
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {showEdgeForm && selectedNodes.length === 2 && (
          <Card className="mb-4">
            <CardHeader>
              <CardTitle>Add Edge</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleEdgeSubmit} className="space-y-4">
                <div>
                  <label className="block mb-2">Relationship</label>
                  <input 
                    id="relationship"
                    type="text"
                    placeholder="Describe the relationship"
                    className="w-full p-2 border rounded"
                    required
                  />
                </div>
                <Button type="submit" className="w-full bg-green-500 hover:bg-green-600">
                  Create Edge
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Lists */}
        <div className="flex-1 overflow-auto">
          <div className="mb-4">
            <h2 className="font-bold mb-2">Nodes</h2>
            <div className="space-y-2">
              {nodes.map(node => (
                <div 
                  key={node.id}
                  className={`p-2 border rounded cursor-pointer ${
                    selectedNodes.includes(node.id) ? 'bg-blue-100 border-blue-500' : ''
                  }`}
                  onClick={() => handleNodeSelect(node.id)}
                >
                  <div className="font-bold">{node.type}</div>
                  <div className="text-sm">
                    {Object.entries(node.properties).map(([key, value]) => (
                      <div key={key}>{key}: {value}</div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="font-bold mb-2">Edges</h2>
            <div className="space-y-2">
              {edges.map(edge => (
                <div key={edge.id} className="p-2 border rounded">
                  Node {edge.source} → Node {edge.target}: {edge.relationship}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main canvas area */}
      <div className="flex-1 bg-gray-50">
        <GraphCanvas nodes={nodes} edges={edges} />
      </div>
    </div>
  );
};

export default GraphBuilder;