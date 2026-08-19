import React, { useState, useEffect, useRef } from 'react';
import {
  BotMessageSquare,
  Sparkles,
  Send,
  User,
  BookOpen,
  HelpCircle,
  ExternalLink,
  ChevronRight,
  PlusCircle,
  CheckCircle2,
  Clock
} from 'lucide-react';
import { chatAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const QUICK_PROMPTS = [
  "I have 3 months before placements. What should I prioritize?",
  "What projects should I build to master PyTorch for AI/ML roles?",
  "How do I write Google XYZ bullet points for my resume?",
  "What are the most common technical interview questions for this role?"
];

export default function AssistantPage() {
  const { user } = useAuth();
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'assistant',
      content: `Hello ${user?.full_name?.split(' ')[0] || 'Rahul'}! I'm your **SkillBridge AI Career Co-Pilot**.\n\nI have full context on your verified skills, semester progress, and target career. How can I help you accelerate your journey today?`,
      sources: []
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const res = await chatAPI.getConversations();
      if (res.data && res.data.length > 0) {
        setConversations(res.data);
        const latest = res.data[0];
        setConversationId(latest.id);
        if (latest.messages && latest.messages.length > 0) {
          setMessages(latest.messages);
        }
      }
    } catch (e) {
      console.error('Error loading previous chats', e);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, sending]);

  const handleStartNewChat = () => {
    setConversationId(null);
    setMessages([
      {
        id: 'welcome',
        sender: 'assistant',
        content: `Hello ${user?.full_name?.split(' ')[0] || 'Rahul'}! Starting a new conversation. What would you like to discuss or plan today?`,
        sources: []
      }
    ]);
  };

  const handleSelectConversation = (conv) => {
    setConversationId(conv.id);
    if (conv.messages && conv.messages.length > 0) {
      setMessages(conv.messages);
    }
  };

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text.trim() || sending) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      content: text,
      sources: []
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setSending(true);

    try {
      const res = await chatAPI.sendMessage(text, conversationId);
      setMessages((prev) => [...prev, res.data]);
      if (res.data.conversation_id && !conversationId) {
        setConversationId(res.data.conversation_id);
      }
    } catch (e) {
      console.error(e);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          content: "I'm having difficulty connecting to the AI service right now. Please check your network or try again.",
          sources: []
        }
      ]);
    } finally {
      setSending(false);
    }
  };

  // Helper to format markdown text with bolding, lists, and headings cleanly
  const renderFormattedContent = (content) => {
    return content.split('\n').map((line, idx) => {
      // Heading 3
      if (line.startsWith('### ')) {
        return (
          <h3 key={idx} className="text-sm font-bold text-indigo-300 mt-2 mb-1">
            {line.replace('### ', '')}
          </h3>
        );
      }
      // Heading 2 / 1
      if (line.startsWith('## ') || line.startsWith('# ')) {
        return (
          <h2 key={idx} className="text-base font-extrabold text-white mt-3 mb-1">
            {line.replace(/^[#]+\s/, '')}
          </h2>
        );
      }
      // List items
      if (line.startsWith('- ') || line.startsWith('* ')) {
        return (
          <li key={idx} className="ml-4 list-disc text-xs sm:text-sm text-slate-200 my-0.5">
            {renderInlineText(line.substring(2))}
          </li>
        );
      }
      // Numbered list
      if (/^\d+\.\s/.test(line)) {
        return (
          <li key={idx} className="ml-4 list-decimal text-xs sm:text-sm text-slate-200 my-0.5">
            {renderInlineText(line.replace(/^\d+\.\s/, ''))}
          </li>
        );
      }
      // Empty line
      if (!line.trim()) {
        return <div key={idx} className="h-1.5" />;
      }
      // Regular paragraph
      return (
        <p key={idx} className="text-xs sm:text-sm text-slate-200 leading-relaxed my-0.5">
          {renderInlineText(line)}
        </p>
      );
    });
  };

  const renderInlineText = (text) => {
    // Basic regex split for bold **text** and code `text`
    const parts = text.split(/(\*\*.*?\*\*|`.*?`)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="text-white font-bold">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return <code key={i} className="px-1.5 py-0.5 rounded bg-white/10 text-indigo-300 font-mono text-xs">{part.slice(1, -1)}</code>;
      }
      return part;
    });
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col glass-panel rounded-3xl border border-white/10 overflow-hidden shadow-2xl animate-in fade-in duration-300">
      {/* Assistant Header */}
      <div className="p-4 sm:p-5 border-b border-white/8 bg-[#0C1220]/80 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/25">
            <div className="w-full h-full bg-[#090D16] rounded-[10px] flex items-center justify-center">
              <BotMessageSquare className="w-5 h-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <h2 className="text-base font-bold font-heading text-white flex items-center gap-2">
              Career Assistant & Mentor
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-bold border border-indigo-500/30">
                RAG Grounded
              </span>
            </h2>
            <p className="text-xs text-slate-400">Context-aware advisor with student profile injection</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleStartNewChat}
            className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-semibold text-slate-300 hover:text-white border border-white/10 flex items-center gap-1.5 transition-colors"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">New Chat</span>
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 p-4 sm:p-6 overflow-y-auto space-y-5">
        {messages.map((m, idx) => {
          const isUser = m.sender === 'user';
          return (
            <div
              key={idx}
              className={`flex items-start gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : ''}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                  isUser
                    ? 'bg-indigo-600 text-white'
                    : 'bg-white/10 text-indigo-300 border border-white/10'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4 text-indigo-400" />}
              </div>

              {/* Message Bubble */}
              <div className={`space-y-2 max-w-2xl ${isUser ? 'items-end' : ''}`}>
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    isUser
                      ? 'bg-gradient-to-r from-indigo-600 to-indigo-500 text-white rounded-tr-none shadow-md shadow-indigo-600/20'
                      : 'bg-white/5 border border-white/8 text-slate-200 rounded-tl-none'
                  }`}
                >
                  {renderFormattedContent(m.content)}
                </div>

                {/* Sources / Citations if any */}
                {m.sources && m.sources.length > 0 && (
                  <div className="p-3 rounded-xl bg-white/2 border border-white/5 space-y-1.5 max-w-md">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                      <BookOpen className="w-3 h-3 text-indigo-400" /> Knowledge Base Grounding:
                    </span>
                    {m.sources.map((s, sIdx) => (
                      <div key={sIdx} className="text-[11px] text-slate-400">
                        <span className="font-semibold text-slate-300">• {s.title}: </span>
                        <span>{s.snippet}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {sending && (
          <div className="flex items-center gap-3 text-xs text-indigo-300 p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20 max-w-md">
            <Sparkles className="w-4 h-4 animate-spin text-indigo-400" />
            <span>AI Co-Pilot is synthesizing personalized career advice...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="px-4 py-2 border-t border-white/5 bg-[#090D16]/60 flex items-center gap-2 overflow-x-auto">
        <span className="text-[10px] uppercase font-bold text-slate-500 shrink-0">Quick Ask:</span>
        {QUICK_PROMPTS.map((prompt, pIdx) => (
          <button
            key={pIdx}
            type="button"
            onClick={() => handleSendMessage(prompt)}
            className="px-3 py-1 rounded-full text-xs bg-white/5 hover:bg-indigo-500/20 hover:text-indigo-300 text-slate-400 border border-white/8 whitespace-nowrap transition-colors"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <div className="p-4 border-t border-white/8 bg-[#0C1220]/90">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center gap-3"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask anything about your career path, missing skills, resume, or projects..."
            className="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white text-xs sm:text-sm focus:outline-none focus:border-indigo-500 placeholder:text-slate-500"
          />
          <button
            type="submit"
            disabled={sending || !inputText.trim()}
            className="px-5 py-3 rounded-xl btn-primary text-white font-bold text-xs flex items-center gap-2 disabled:opacity-50 shrink-0"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
