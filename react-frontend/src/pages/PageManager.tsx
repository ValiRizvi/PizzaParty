import React, { useState } from 'react';

import PostalCodeForm from '../components/postal_code/PostalCodeForm';
import BestValueButton from '../components/best_value/BestValueButton';
import MostSimilar from '../components/most_similar/MostSimilar';

import '../styles/SplitScreen.css';


const PageManager: React.FC = () => {

    const [postalCodeValid, setPostalCodeValid] = useState<boolean>(false);
    const [localStores, setLocalStores] = useState<any>(null);
    const [allCoupons, setAllCoupons] = useState<any>(null);
    
    
    const handleValidSubmission = (valid: boolean, local_stores: any, allCoupons: any) => {
        setPostalCodeValid(valid);
        if (local_stores) {
            setLocalStores(local_stores);
            setAllCoupons(allCoupons);
        };
    };
    

    return (
        <div>

            {postalCodeValid ? ( 
                <div className="split-screen">

                    <div className="split-box split-box-left">
                        <BestValueButton local_stores={localStores} allCoupons={allCoupons} />
                    </div>


                    <div className="split-box split-box-right">
                        <MostSimilar local_stores={localStores} allCoupons={allCoupons} />
                    </div>

                </div>
            ) : (
                <PostalCodeForm onValidSubmission={handleValidSubmission} />
            )}

        </div>
    );
};

export default PageManager;