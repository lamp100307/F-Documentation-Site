import React, { useState } from 'react';
import './App.css';

function App() {
    const [name, setName] = useState('');
    const [question, setQuestion] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault(); // Предотвращаем перезагрузку страницы

        if (!name.trim() || !question.trim()) {
            alert('Пожалуйста, заполните оба поля.');
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
                const data = await response.json();
                setMessage(`Спасибо, ${data.name}! Ваш вопрос принят.`);
                setName('');
                setQuestion('');
            } else {
                setMessage('Произошла ошибка при отправке вопроса. Попробуйте ещё раз.');
            }
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            setMessage('Произошла ошибка при подключении к серверу.');
        }
    };

    return (
        <div className="App">
            <h1>Форма вопроса</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="nameInput">Имя:</label>
                    <input
                        id="nameInput"
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="questionInput">Вопрос:</label>
                    <textarea
                        id="questionInput"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        style={{ height: 'auto' }}
                        onInput={(e) => {
                            e.target.style.height = 'auto';
                            e.target.style.height = `${e.target.scrollHeight}px`;
                        }}
                    />
                </div>
                <button type="submit">Отправить</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default App;
