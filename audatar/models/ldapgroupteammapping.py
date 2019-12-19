from audatar.extensions import db


class LdapGroupTeamMapping(db.Model):
    __tablename__ = 'ldapgroupteammappings'
    id = db.Column(db.Integer, primary_key=True)
    ldap_group = db.Column(db.String(128), unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team')

    def __repr__(self):
        return '<ldapgroupteammapping %r>' % (self.ldap_group)
