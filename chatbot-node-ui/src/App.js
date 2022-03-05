import './App.css';

import ChatBot from 'react-simple-chatbot';

function App() {
  return (
    <div className="App"
      style={{
        position: 'absolute', left: '50%', top: '50%',
        transform: 'translate(-50%, -50%)'
    }}
    >
      <ChatBot
        style = {{width: '600px'}}
        headerTitle = "Sahay"
        steps={[
          {
            id: '1',
            message: 'Hi! Welcome to Sahay - AI based Legal Assistance chatbot',
            trigger: '2',
          },
          {
            id: '2',
            message: 'Is your grievance related to a good or a service?',
            trigger: '3',
          },
          {
            id: '3',
            options: [
              { value: 1, label: 'Goods', trigger: '4' },
              { value: 2, label: 'Service', trigger: '5' },
              { value: 3, label: "Don't know", trigger: '6' },
            ],
          },
          {
            id: '4',
            message: 'Goods',
            end: true,
          },
          {
            id: '5',
            message: 'Services',
            end: true,
          },
          {
            id: '6',
            message: 'Is your grievance related to a movable property including food?',
            trigger: '7',
          },
          {
            id: '7',
            message: 'end',
            end: true,
          },
        ]}
      />
    </div>
  );
}

export default App;
