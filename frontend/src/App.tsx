import React, { useState, ChangeEvent, FormEvent, useEffect } from 'react';
import './App.css';

interface ResponseData {
    name: string;
}

function App() {
    const [name, setName] = useState<string>('');
    const [question, setQuestion] = useState<string>('');
    const [message, setMessage] = useState<string>('');
    const [messageType, setMessageType] = useState<'success' | 'error' | ''>(''); // Тип сообщения

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault(); // Предотвращаем перезагрузку страницы

        if (!name.trim() || !question.trim()) {
            setMessage('Пожалуйста, заполните оба поля.');
            setMessageType('error');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, question }),
            });

            if (response.ok) {
                const data: ResponseData = await response.json();
                setMessage(`Спасибо, ${data.name}! Ваш вопрос принят.`);
                setMessageType('success');
            } else {
                setMessage('Произошла ошибка при отправке вопроса. Попробуйте ещё раз.');
                setMessageType('error');
            }
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            setMessage('Произошла ошибка при подключении к серверу.');
            setMessageType('error');
        }
    };

    const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value);
    };

    const handleQuestionChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        setQuestion(e.target.value);
    };

    // Эффект для скрытия сообщения через 2 секунды
    useEffect(() => {
        if (message) {
            const timer = setTimeout(() => {
                setMessage('');
                setMessageType('');
            }, 2000);

            return () => clearTimeout(timer); // Очистка таймера
        }
    }, [message]);

    return (
        <div className="App">
            <h1>Форма вопроса</h1>
            <form onSubmit={handleSubmit} className="Inputs">
                <div>
                    <input
                        id="nameInput"
                        type="text"
                        placeholder="Ваше имя:"
                        value={name}
                        onChange={handleNameChange}
                    />
                </div>
                <div>
                    <textarea
                        id="questionInput"
                        value={question}
                        onChange={handleQuestionChange}
                        style={{ height: 'auto' }}
                        placeholder="Ваш вопрос:"
                        onInput={(e) => {
                            e.target.style.height = 'auto';
                            e.target.style.height = `${e.target.scrollHeight}px`;
                        }}
                    />
                </div>
                <button type="submit">Отправить</button>
            </form>

            {message && (
                <div
                    className={`message ${messageType === 'success' ? 'message-success' : 'message-error'} ${message ? '' : 'hide'}`}
                >
                    {message}
                </div>
            )}
        </div>
    );
}

export default App;
