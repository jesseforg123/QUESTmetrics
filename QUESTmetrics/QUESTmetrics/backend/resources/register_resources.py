from resources.students import (StudentResource, StudentByUIDResource, StudentByDirectoryIdResource, StudentGroupResource,
StudentByUIDGroupResource, StudentByDirectoryIdGroupResource)
from resources.classes import ClassResource, ClassesByDirectoryIdResource
from resources.groups import (GroupsByClassResource, GroupsByStudentUIDResource, GroupsByStudentDirectoryIdResource,
GroupResource, WatchResource, GroupHealthResource, GroupHealthScoreResource, GroupRedResource, GroupsWatchedResource)
from resources.data import GroupBasedDataResource, StudentBasedDataByUIDResource, StudentBasedDataByDirectoryIdResource, ClearResource, ElmsResource, SlackResource
from resources.auth import AuthResource
from resources.weights import WeightsResource
from resources.survey import SurveyResource, StudentResponseResource, QuestionResource
from resources.mock import MockData
from resources.history import HistoryAllResource, HistoryByClassResource
from resources.metrics import Metrics


def registerResources (api):
    # ---- Clear All Tables --- #
    api.add_resource(ClearResource, '/clear')

    # ---- Students ---- #
    api.add_resource(StudentResource, '/students')
    api.add_resource(StudentByUIDResource, '/student/uid/<uid>')
    api.add_resource(StudentByDirectoryIdResource, '/student/directoryId/<directoryId>')
    api.add_resource(StudentGroupResource, '/students/group/<name>')
    api.add_resource(StudentByUIDGroupResource, '/student/uid/<uid>/group/<name>')
    api.add_resource(StudentByDirectoryIdGroupResource, '/student/directoryId/<directoryId>/group/<name>')

    # ---- Groups ---- #
    api.add_resource(GroupResource, '/groups')
    #TODO: implement email functionality for toggled groups
    api.add_resource(WatchResource, '/group/watch/<name>')
    api.add_resource(GroupsByClassResource, '/groups/class/<className>')
    api.add_resource(GroupHealthResource, '/group/health/<name>')
    api.add_resource(GroupHealthScoreResource, '/group/score/<name>')
    api.add_resource(GroupRedResource, '/groups/red')
    api.add_resource(GroupsByStudentDirectoryIdResource, '/groups/student/directoryId/<directoryId>')
    api.add_resource(GroupsByStudentUIDResource, '/groups/student/uid/<uid>')
    api.add_resource(GroupsWatchedResource, '/groups/watching')
    api.add_resource(Metrics, '/metrics')


    # ---- Classes ---- #
    api.add_resource(ClassResource, '/classes')
    api.add_resource(ClassesByDirectoryIdResource, '/classes/student/directoryId/<directoryId>')

    # ---- Data ---- #
    api.add_resource(ElmsResource, '/elms')
    api.add_resource(SlackResource, '/slack/group/<name>')
    api.add_resource(GroupBasedDataResource, '/<table>/group/<name>')
    api.add_resource(StudentBasedDataByUIDResource, '/<table>/student/uid/<uid>/class/<className>')
    api.add_resource(StudentBasedDataByDirectoryIdResource, '/<table>/student/directoryId/<directoryId>/class/<className>')

    # ---- AUTH ---- #
    api.add_resource(AuthResource, '/auth')

    # ---- Weights ---- #
    api.add_resource(WeightsResource, '/weights')

    # ---- Survey ---- #
    api.add_resource(SurveyResource, '/survey/class/<className>')
    api.add_resource(StudentResponseResource, '/survey/class/<className>/student/directoryId/<directoryId>')
    api.add_resource(QuestionResource, '/survey/questions/class/<className>')

    # ---- History ---- #
    api.add_resource(HistoryAllResource, '/survey/history')
    api.add_resource(HistoryByClassResource, '/survey/history/class/<className>')

    # Mock
    api.add_resource(MockData, '/mock')
