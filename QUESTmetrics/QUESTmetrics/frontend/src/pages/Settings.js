import React, { useState, useEffect } from 'react';
import { useRouteMatch } from 'react-router-dom';
import { fetchWeight, postMetrics, postWeight, deleteWeight } from '../utils/fetch';
import { useHistory } from 'react-router-dom';

const Settings = () => {
	const [metrics, setMetrics] = useState({});
	const [loaded, setLoaded] = useState(false);
	const { url } = useRouteMatch();

	useEffect(() => {
		(async () =>
			await fetchWeight().then(data => {
				setMetrics(data);
				setLoaded(true);
			}))();
	}, [url]);

	const handleWeightChange = e => {
		const isNumeric = str => {
			if (typeof str != 'string') return false;
			return !isNaN(str);
		};
		if (isNumeric(e.target.value)) {
			let newMetrics = { ...metrics };
			newMetrics[e.target.name] = e.target.value;
			setMetrics(newMetrics);
		}
	};

	const removeElements = elms => elms.forEach(el => el.remove());

	const postWeights = async e => {
		e.preventDefault();
		document.querySelector('.success').innerHTML = '';
		var sum = Object.values(metrics).reduce(function (a, b) {
			return Number(a) + Number(b);
		}, 0);
		console.log(sum);
		if (sum === 100 || sum === '100') {
			(async () => await postWeight(metrics))();
			removeElements(document.querySelectorAll('.errormessage'));
			postMetrics();
			let success = document.querySelector('.successmessage');
			if (success == null) {
				success = document.createElement('h3');
				success.className = 'successmessage';
				success.innerText = `Your weights have been recorded.`;
				success.style = ` color: green; margin-left: 0.6rem;line-height: 2.5rem; `;
				document.querySelector('.settings').appendChild(success);
			} else {
				success.innerText = `Your weights have been recorded.`;
			}
			//REDIRECT
		} else {
			let error = document.querySelector('.errormessage');
			removeElements(document.querySelectorAll('.successmessage'));
			if (error == null) {
				document.querySelector('.success').innerHTML = '';
				error = document.createElement('h3');
				error.className = 'errormessage';
				error.innerText = `ERROR:\nYour values do not add up to a 100, but they instead add up to ${sum}. Your weights have not been saved!\nPlease fix your weights and try again.`;
				error.style = ` color: red; margin-left: 0.6rem;line-height: 2.5rem; `;
				document.querySelector('.settings').appendChild(error);
			} else {
				error.innerText = `ERROR:\nYour values do not add up to a 100, but they instead add up to ${sum}. Your weights have not been saved!\nPlease fix your weights and try again.`;
			}
		}
	};

	const update = e => {
		postWeights(e);
	};


	const deleteWeights = e => {
		removeElements(document.querySelectorAll('.successmessage'));
		removeElements(document.querySelectorAll('.errormessage'));
		let newMetrics = { ...metrics };
		newMetrics["slack"] = 20;
		newMetrics["grades"] = 15;
		newMetrics["lateness"] = 17.5;
		newMetrics["survey"] = 30;
		newMetrics["lastView"] = 17.5;
		setMetrics(newMetrics);
	};

	const settings = Object.keys(metrics).map(metric => (
		<div key={metric} className="metrics">
			<div className="metric">{metric.charAt(0).toUpperCase() + metric.slice(1)}</div>
			<input
				type="text"
				name={metric}
				className="weight"
				value={metrics[metric]}
				onChange={e => handleWeightChange(e)}
			/>
		</div>
	));

	return (
		<div className="settingsPage">
			<h1 className="settings-title">Settings</h1>
			<div className="settings">
				{settings}
				{loaded && (
					<div className="save-metrics" onClick={update}>
						Save
					</div>
				)}
				<p className="success"> </p>
			</div>

			<div className = "description">
			<p>
				In this page, you can change the weights of each element included in the
				calculation of the metrics.
				<br />
				<span className="subtext">
					This allows you to customize the calculated health of each team.
				</span>
				<br />
				<br />
				<span className="please">
					Please ensure that your calculations add up to 100.
				</span>
			</p>

			<div className= "default-button" onClick={deleteWeights}>
					Default Metrics
				</div>
			</div>

		</div>
	);
};

export default Settings;
