import jwt_decode from 'jwt-decode';

//const token =
//	'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDczODU2NDcsIm5iZiI6MTYwNzM4NTY0NywianRpIjoiMDg3ZDllZjMtZGI1OC00Nzg1LWExODUtNzk3YjQwY2NlZmQ2IiwiZXhwIjoxNjA3NDcyMDQ3LCJpZGVudGl0eSI6eyJkaXJlY3RvcnlJZCI6InJvaGl0aHYiLCJwcml2aWxlZ2UiOiJhZG1pbiJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.8hUy9hS9au0SxmO_NENldBptqyQNfwUL6aoLZZvWLFA';
//console.log(window.localStorage.token, 'this the student token');

//* CRUD w/ auth token //

//const headers = new Headers({ Authorization: `Bearer ${token}` });
//const get = { method: 'GET', headers: headers };
//const put = { method: 'PUT', headers: headers };
//const post = { method: 'POST', headers: headers };
//const del = { method: 'DELETE', headers: headers };

//* GET //

export const fetchRedGroups = async () => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(`http://valerian.cs.umd.edu:5000/groups/red`, get);
	const data = await response.json();
	return data;
};

export const fetchWatchedGroups = async () => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(`http://valerian.cs.umd.edu:5000/groups/watching`, get);
	const data = await response.json();
	return data;
};

export const fetchAllGroups = async () => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(`http://valerian.cs.umd.edu:5000/groups`, get);
	const data = await response.json();
	return data;
};

export const fetchGroupsInClass = async classname => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/groups/class/${classname}`,
		get
	);
	const data = await response.json();
	return data;
};

export const fetchStudentsInGroup = async groupname => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/students/group/${groupname}`,
		get
	);
	const data = await response.json();
	return data;
};

export const fetchAllClasses = async () => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(`http://valerian.cs.umd.edu:5000/classes`, get);
	const data = await response.json();
	return data;
};

export const fetchWeight = async () => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(`http://valerian.cs.umd.edu:5000/weights`, get);
	const data = await response.json();
	return data;
};

export const fetchSurvey = async classname => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/survey/questions/class/${classname}`,
		get
	);
	const data = await response.json();
	return data;
};

export const fetchGroupHealth = async groupname => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const get = { method: 'GET', headers: headers };
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/group/health/${groupname}`,
		get
	);
	const data = await response.json();
	return data;
};

//* DELETE //
export const deleteWeight = async metrics => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const del = { method: 'DELETE', headers: headers };
	const url = new URL(`http://valerian.cs.umd.edu:5000/weights`);
	const response = await fetch(url, del);
	// console.log(response);
};

//* POST //

export const watchGroup = async groupname => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const post = { method: 'POST', headers: headers };
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/group/watch/${groupname}`,
		post
	);
	console.log(response);
};

export const postMetrics = async metrics => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const put = { method: 'PUT', headers: headers };
	const url = new URL(`http://valerian.cs.umd.edu:5000/metrics`);
	// Object.keys(metrics).forEach(key => url.searchParams.append(key, metrics[key]));
	const response = await fetch(url, put);
	// console.log(response);
};

export const postWeight = async metrics => {
	const token = window.localStorage.token;
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const put = { method: 'PUT', headers: headers };
	// console.log(metrics);
	const url = new URL(`http://valerian.cs.umd.edu:5000/weights`);
	Object.keys(metrics).forEach(key => url.searchParams.append(key, metrics[key]));
	const response = await fetch(url, put);
	// console.log(response);
};

export const postSurvey = async (questions, surveyClass) => {
	const token = window.localStorage.token;
	const classes = ['BMGT390H', 'BMGT438A', 'BMGT490H'];
	const headers = new Headers({ Authorization: `Bearer ${token}` });
	const del = { method: 'DELETE', headers: headers };
	const headers2 = new Headers({
		Authorization: `Bearer ${token}`,
		'Content-Type': 'application/json',
	});
	const obj = {
		method: 'POST',
		headers: headers2,
		body: JSON.stringify(questions),
		mode: 'cors',
	};

	if (surveyClass == 'ALL') {
		classes.forEach(async c => {
			console.log('pls');
			const url = new URL(`http://valerian.cs.umd.edu:5000/survey/class/${c}`);
			await fetch(url, del); // delete existing surveys
			const response = await fetch(url, obj); // post new survey
			console.log(response);
		});
	} else {
		const url = new URL(`http://valerian.cs.umd.edu:5000/survey/class/${surveyClass}`);
		await fetch(url, del); // delete existing survey
		const response = await fetch(url, obj); // post new survey
		console.log(response.text());
	}
};

export const postSurveyStudentAnswers = async (classname, answers, token) => {
	//const token = window.localStorage.token;
	const dirid = jwt_decode(token)['identity']['directoryId'];

	const headers2 = new Headers({
		Authorization: `Bearer ${token}`,
		'Content-Type': 'application/json',
	});
	const obj = { method: 'PUT', headers: headers2, body: JSON.stringify(answers) };

	console.log(answers);

	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/survey/class/${classname}/student/directoryId/${dirid}`,
		obj
	);
	console.log(response);
};

export const getClassesofStudent = async () => {
	const dirid = jwt_decode(window.localStorage.token)['identity']['directoryId'];

	const headers = new Headers({ Authorization: `Bearer ${window.localStorage.token}` });

	// console.log(dirid, 'this the student dirid');
	const response = await fetch(
		`http://valerian.cs.umd.edu:5000/classes/student/directoryId/${dirid}`,
		{ method: 'GET', headers }
	);

	const data = await response.json();
	return data;
};
