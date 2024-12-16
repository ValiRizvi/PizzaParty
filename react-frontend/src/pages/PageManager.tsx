import React, { useState } from 'react';

import PostalCodeForm from '../components/PostalCodeForm';

import '../styles/SplitScreen.css';

const PageManager: React.FC = () => {

    const [postalCodeValid, setPostalCodeValid] = useState<boolean>(false);

    return (
        <div>
            {postalCodeValid ? ( 
                <div className="split-screen">
                    <div className="split-screen">
                        <div className="split-box split-box-left">
                            <h2>Best Value</h2>
                        </div>
                    </div>
                    <div className="split-screen">
                        <div className="split-box split-box-right">
                            <h2>AI</h2>
                        </div>
                    </div>
                </div>
            ) : (
                <PostalCodeForm onValidSubmission={setPostalCodeValid} />
            )}
        </div>
    );
};

export default PageManager;