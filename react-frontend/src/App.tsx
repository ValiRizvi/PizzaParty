import PageManager from './pages/PageManager.tsx';
import Background from './components/Background.tsx';

import '../src/styles/App.css';

function App() {
  return (
    <div className='app'>
      <Background /> 
      <div className='blur-layer'></div>

      <div className='content'>
        <PageManager />
      </div>
    </div>
  )
};

export default App;
