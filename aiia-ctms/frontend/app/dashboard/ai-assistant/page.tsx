import React, { useState } from 'react';

export default function AIAssistantPage() {
    const [input, setInput] = useState('');
    const [chat, setChat] = useState([
        { role: 'ai', text: 'Hello Dr. Vansh. I am Gemma 4. How can I help you with your clinical trials today?' }
    ]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;
        
        const userMsg = { role: 'user', text: input };
        setChat(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/ai/extract', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: input })
            });
            const data = await response.json();
            setChat(prev => [...prev, { role: 'ai', text: `Analysis Result:\n${JSON.stringify(JSON.parse(data.data), null, 2)}` }]);
        } catch (e) {
            setChat(prev => [...prev, { role: 'ai', text: 'Error connecting to AI service. Please ensure Ollama is running.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-slate-100 p-6">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 bg-white rounded-2xl shadow-inner">
                {chat.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xl p-4 rounded-2xl ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-800'}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-slate-400 italic animate-pulse">Gemma 4 is thinking...</div>}
            </div>
            <div className="flex gap-4">
                <input 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    className="flex-1 p-4 rounded-xl border focus:ring-2 focus:ring-blue-500 outline-none shadow-sm"
                    placeholder="Ask about trial protocols, risk analysis or safety data..."
                />
                <button 
                    onClick={sendMessage}
                    className="bg-blue-600 text-white px-6 py-4 rounded-xl font-bold hover:bg-blue-700 transition"
                >
                    Send
                </button>
            </div>
        </div>
    );
}
