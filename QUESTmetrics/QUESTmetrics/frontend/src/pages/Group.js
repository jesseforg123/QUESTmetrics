import React, { useState, useEffect } from 'react';
import { useParams, useRouteMatch } from 'react-router-dom';
import Collapsible from 'react-collapsible';
import {
	fetchStudentsInGroup,
	fetchWatchedGroups,
	watchGroup,
	fetchGroupHealth,
} from '../utils/fetch';

const Group = () => {
	const [studentsInGroup, setStudents] = useState({});
	const [watchedGroups, setWatchedGroups] = useState({});
	const [groupColor, setGroupColor] = useState(null);
	const { groupname } = useParams();
	const { url } = useRouteMatch();

	// useEffect(() => window.location.reload(), []);

	useEffect(() => {
		(async () => {
			await fetchStudentsInGroup(groupname).then(data => setStudents(data));
			await fetchWatchedGroups().then(data => setWatchedGroups(data));
			await fetchGroupHealth(groupname).then(data => {
				const health = data['result'];
				if (health == 1) setGroupColor('indianred');
				else if (health == 2) setGroupColor('khaki');
				else setGroupColor('lightgreen');
			});
		})();
	}, [url, watchedGroups, groupname]);

	const students = Object.keys(studentsInGroup).map(s => {
		const { firstName, lastName, directoryId, uid } = studentsInGroup[s];
		return (
			<div className="studentInGroup">
				<div>
					{lastName}, {firstName}
				</div>
				<div>{directoryId}</div>
				<div>{uid}</div>
			</div>
		);
	});

	const vislinks = {
		'Team 1 (RecyclePoints - Nigeria)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team1RecyclePoints-Nigeria',
		'Team 2 (Kaaro Health - Uganda)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team2KaaroHealth-Uganda',
		'Team 3 (Expressions - Kenya)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team3Expressions-Kenya',
		'Team 4 (Rafode - Kenya)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team4Rafode-Kenya',
		'Team 5 (Ruo and Rui Medical - South Africa)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team5RuoandRuiMedical-SouthAfrica',
		'Team 6 (Ecobora - Kenya)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team6Ecobora-Kenya',
		'Team 7 (CODE - Uganda)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team7CODE-Uganda',
		'Team 8 (Crispvision - Nigeria)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team8Crispvision-Nigeria',
		'Team 9 (Fort Garlic Farm - Uganda)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team9FortGarlicFarm-Uganda',
		'Team 10 (East Wind - Nigeria)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/Team10EastWind-Nigeria',
		'1 Ctrl Alt QUEST - QUEST Honors Program (Kohn)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/1CtrlAltQUEST-QUESTHonorsProgramKohn',
		'2 Q\u200brystal Cl\u200b34\u200br - ClearSage (Bailey)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/2Qu200brystalClu200b34u200br-ClearSageBailey',
		'3 QUESTees Care - Casey Cares (Wertman)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/3QUESTeesCare-CaseyCaresWertman',
		'4 QuestBytes - WorkChew (Kohn)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/4QuestBytes-WorkChewKohn',
		'5 LochQUEST Monster - Chessie Marine (King)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/5LochQUESTMonster-ChessieMarineKing',
		'6 mapQUEST - Campus Maps (Armstrong)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/6mapQUEST-CampusMapsArmstrong',
		'7 Never Second QUEST - Bechtel (King)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/7NeverSecondQUEST-BechtelKing',
		'8 QUESTainability - UMD Facilities (Bailey)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/8QUESTainability-UMDFacilitiesBailey',
		'9 Key West - Smith Operations (Armstrong)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/9KeyWest-SmithOperationsArmstrong',
		'Casey Cares Foundation (Frels)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/CaseyCaresFoundationFrels',
		"Children's National Hospital (Dugas)":
			"http://valerian.cs.umd.edu:8080/superset/dashboard/Children'sNationalHospitalDugas",
		'Leidos (Ashley)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/LeidosAshley',
		'Materne North America - GoGo squeeZ (Corsi)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/MaterneNorthAmerica-GoGosqueeZCorsi',
		'Northrop Grumman (A) - Financial Tools (Karake)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/NorthropGrummanA-FinancialToolsKarake',
		'Northrop Grumman (B) - Supplier Ratings (Armstrong)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/NorthropGrummanB-SupplierRatingsArmstrong',
		'Oceaneering (Bailey)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/OceaneeringBailey',
		'Sealed Air (White)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/SealedAirWhite',
		'Thales (Purtilo)':
			'http://valerian.cs.umd.edu:8080/superset/dashboard/ThalesPurtilo',
		'Tronox (Basu)': 'http://valerian.cs.umd.edu:8080/superset/dashboard/TronoxBasu',
	};

	const onoffswitch = state => (
		<div class="onoffswitch">
			<input
				type="checkbox"
				name="onoffswitch"
				class="onoffswitch-checkbox"
				id="myonoffswitch"
				tabindex="0"
				checked={state}
				onClick={() => watchGroup(groupname)}
			/>
			<label class="onoffswitch-label" for="myonoffswitch">
				<span class="onoffswitch-inner"></span>
				<span class="onoffswitch-switch"></span>
			</label>
		</div>
	);

	return (
		<div>
			<div className="group-title">
				<h2
					className="group-name"
					style={{
						background: `${groupColor}`,
						color: '#333',
						borderRadius: '1rem',
						padding: '1rem',
					}}>
					{groupname}
				</h2>
				{Object.keys(watchedGroups)
					.map(g => watchedGroups[g].name)
					.includes(groupname)
					? onoffswitch(true)
					: onoffswitch(false)}
			</div>
			<div className="info">
				<Collapsible trigger="Visualizations">
					<iframe
						className="group-vis"
						title={vislinks[groupname]}
						width="97%"
						height="600px"
						seamless
						frameBorder="0"
						scrolling="yes"
						src={vislinks[groupname]}></iframe>
				</Collapsible>
				<Collapsible trigger="Students">
					<div className="studentsInGroup">{students}</div>
				</Collapsible>
			</div>
		</div>
	);
};

export default Group;
