import React from 'react';
import '../styles/Background.css';


const Background: React.FC = () => {
    
    const triangles: number[] = [];
    for (let i = 0; i < 50; i++) {
        triangles.push(Math.floor(Math.random() * 40));
    }
    

    return (
        <div className='background'>
            <div className='triangles'>
                {triangles.map((i, index) => (
                    <span 
                        key={index} 
                        style={{
                            // random i (animation duration), x/y values and rotation value
                            '--i': `${i}`,
                            '--x': `${Math.random() * 100}vw`, 
                            '--y': `${Math.random() * 100}vh`,   
                            '--rotation': `${Math.floor(Math.random() * 360)}deg`
                        } as React.CSSProperties} 
                    ></span>
                ))}
            </div>
        </div>
    );
};

export default Background;
