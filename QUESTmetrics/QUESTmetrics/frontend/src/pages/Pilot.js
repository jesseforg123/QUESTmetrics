import React, { useEffect } from 'react';

function Pilot() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://prod-useast-b.online.tableau.com/javascripts/api/viz_v1.js';
    script.async = true;
    document.body.appendChild(script);
  });

  return (
    <div>
      <h1> Pilot Sample Data</h1>
      <h3>
        This data is from the QUESTMetrics slack channel to demonstrate that we can
        connect to Tableau and display the data
      </h3>
      <div className="tableauPlaceholder" style={{ width: '1280px', height: '666px' }}>
        <object className="tableauViz" width="1280px" height="666px">
          <param
            name="host_url"
            value="https%3A%2F%2Fprod-useast-b.online.tableau.com%2F"
          />{' '}
          <param name="embed_code_version" value="3" />{' '}
          <param name="site_root" value="&#47;t&#47;questmetrics" />
          <param name="name" value="Playground&#47;Sheet1" />
          <param name="tabs" value="no" />
          <param name="toolbar" value="yes" />
          <param name="showAppBanner" value="false" />
        </object>
      </div>
    </div>
  );
}

export default Pilot;
