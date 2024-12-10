import PostalCodeScreen from './pages/PostalCodeScreen';
import Background from './components/Background';

import '../src/styles/App.css';

function App() {
  return (
    <div className='app'>
      <Background /> 
      <div className='blur-layer'></div>

      <div className='content'>
        <PostalCodeScreen />
      </div>
    </div>
  )
};

export default App;
