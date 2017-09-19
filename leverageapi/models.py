# coding: utf-8
# Baseline generated by sqlacodegen mysql://leverage:leverage_pass@localhost/leverage_philly

from .database import Base, db_session as session
import sqlalchemy as sa
from sqlalchemy.orm import synonym
from sqlalchemy.dialects.mysql import ENUM, YEAR



class Candidate(Base):
    __tablename__ = 'candidate'

    id = sa.Column(sa.Integer, primary_key=True)
    party_id = sa.Column(sa.Integer, nullable=False)
    fec_id = sa.Column(sa.String(9), index=True)
    district = sa.Column(sa.Integer, nullable=False)
    name_first = sa.Column(sa.String(128), nullable=False)
    name_middle = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    name_last = sa.Column(sa.String(32), nullable=False)
    name_suffix = sa.Column(sa.String(8), nullable=False, server_default=sa.text("''"))
    slug = sa.Column(sa.String(64), nullable=False)
    website = sa.Column(sa.String(128), nullable=False, server_default=sa.text("''"))
    social_blob = sa.Column(sa.Text, nullable=False)
    is_active = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'1'"))
    candidate_order = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    def __repr__(self):
        return '<Candidate %r %r>' % (self.name_first, self.name_last)
    
    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['candidacies'] = [c.as_dict() for c in self.candidacies]
        return d


class Candidacy(Base):
    __tablename__ = 'candidacy'

    id = sa.Column(sa.Integer, primary_key=True)

    candidate_id = sa.Column(sa.Integer, nullable=False, index=True)
    candidate = sa.orm.relationship('Candidate', 
                                    primaryjoin='Candidacy.candidate_id==Candidate.id',
                                    foreign_keys='Candidacy.candidate_id',
                                    remote_side='Candidate.id',
                                    backref='candidacies')

    race_id = sa.Column(sa.Integer, nullable=False, index=True)
    race = sa.orm.relationship('Race', 
                                    primaryjoin='Candidacy.race_id==Race.id',
                                    foreign_keys='Candidacy.race_id',
                                    remote_side='Race.id',
                                    backref='candidacies')

    candidacy_type = sa.Column(ENUM(u'incumbent', u'challenger'), nullable=False, index=True)
    outcome = sa.Column(ENUM(u'won', u'lost'), nullable=False)

    def __repr__(self):
        return '<Candidacy %r %r, (%r %r)>' % (self.candidate.name_first, 
                                               self.candidate.name_last, 
                                               self.race.election_year,
                                               self.race.election_type)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


candidate_committees = sa.Table('candidate_committees', Base.metadata,
                       sa.Column('candidate_id', sa.Integer),
                       sa.Column('committee_id', sa.Integer)
)

"""
class CandidateFiling(Base):
    __tablename__ = 'candidate_filing'

    id = sa.Column(sa.Integer, primary_key=True)
    in_general = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    candidate_id = sa.Column(sa.Integer, nullable=False)
    full_name = sa.Column(sa.String(255), nullable=False)
    office = sa.Column(sa.String(128), nullable=False)
    office_district = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    county = sa.Column(sa.String(2), nullable=False)
    party = sa.Column(sa.String(32), nullable=False)
    address = sa.Column(sa.String(255), nullable=False)
    mail_address = sa.Column(sa.String(128), nullable=False)
    email = sa.Column(sa.String(128), nullable=False)
    url = sa.Column(sa.String(128), nullable=False)
    phone = sa.Column(sa.String(20), nullable=False)
    date_filed = sa.Column(sa.DateTime, nullable=False)
    date_found = sa.Column(sa.DateTime, nullable=False)
    page_found = sa.Column(sa.String(16), nullable=False)
"""

class Committee(Base):
    __tablename__ = 'committee'

    id = sa.Column(sa.Integer, primary_key=True)
    candidate_id = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    is_candidates = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    committee_name = sa.Column(sa.String(128), nullable=False, unique=True)
    committee_slug = sa.Column(sa.String(128), index=True)
    committee_description = sa.Column(sa.Text)
    donations_2015 = sa.Column(sa.Numeric(10, 2), server_default=sa.text("'0.00'"))
    donations_2016 = sa.Column(sa.Numeric(10, 2), server_default=sa.text("'0.00'"))

    candidates = sa.orm.relationship('Candidate',
                                     primaryjoin='Committee.id==candidate_committees.c.committee_id',
                                     secondaryjoin='candidate_committees.c.candidate_id==Candidate.id',
                                     secondary=candidate_committees,
                                     backref='committees')

    def __repr__(self):
        return '<Committee %r>' % self.committee_name

    def as_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['candidates'] = [o.as_dict() for o in self.candidates]





class ContributorAddres(Base):
    __tablename__ = 'contributor_address'
    __table_args__ = (
        sa.Index('city', 'city', 'state'),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    address_type = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    number = sa.Column(sa.String(16), nullable=False, index=True, server_default=sa.text("''"))
    street = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    addr1 = sa.Column(sa.String(128), nullable=False, index=True, server_default=sa.text("''"))
    addr2 = sa.Column(sa.String(128), nullable=False, server_default=sa.text("''"))
    po_box = sa.Column(sa.String(16), nullable=False, server_default=sa.text("''"))
    city = sa.Column(sa.String(64), nullable=False, server_default=sa.text("''"))
    state = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    zipcode = sa.Column(sa.String(16), nullable=False, index=True, server_default=sa.text("''"))
    slug = sa.Column(sa.String(64), unique=True)
    num_individual_contribs = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    num_non_individual_contribs = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    def __repr__(self):
        return '<ContributorAddres %r %r>' % (self.id, self.addr1)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class ContributorType(Base):
    __tablename__ = 'contributor_type'

    id = sa.Column(sa.Integer, primary_key=True)
    type_name = sa.Column(sa.String(64), nullable=False, unique=True)
    type_slug = sa.Column(sa.String(32), nullable=False, index=True, server_default=sa.text("''"))
    type_description = sa.Column(sa.Text)

    def __repr__(self):
        return '<ContributorType %r %r, (%r %r)>' % (self.type_name)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Contributor(Base):
    __tablename__ = 'contributor'

    id = sa.Column(sa.Integer, primary_key=True)
    address_id = sa.Column(sa.Integer, nullable=False, index=True, server_default=sa.text("'0'"))
    address = sa.orm.relationship('ContributorAddres', 
                                    primaryjoin='Contributor.address_id==ContributorAddres.id',
                                    foreign_keys='Contributor.address_id',
                                    remote_side='ContributorAddres.id',
                                    backref='contributors')

    name_prefix = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    name_first = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    name_middle = sa.Column(sa.String(64), nullable=False, server_default=sa.text("''"))
    name_last = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    name_suffix = sa.Column(sa.String(64), nullable=False, index=True, server_default=sa.text("''"))
    name_business = sa.Column(sa.String(255), nullable=False, server_default=sa.text("''"))
    slug = sa.Column(sa.String(64), unique=True)
    is_person = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    is_business = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    num_contributions = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    num_committees_contrib_to = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    total_contributed_2015 = sa.Column(sa.Numeric(12, 2))
    total_contributed_2016 = sa.Column(sa.Numeric(12, 2))

    def __repr__(self):
        return '<Contributor %r %r>' % (self.name_first, 
                                               self.name_last)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




class Party(Base):
    __tablename__ = 'party'

    id = sa.Column(sa.Integer, primary_key=True)
    party_name = sa.Column(sa.String(32), nullable=False)
    slug = sa.Column(sa.String(32), nullable=False)
    party_order = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    def __repr__(self):
        return '<Party %r>' % (self.party_name)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}




class PoliticalDonation(Base):
    __tablename__ = 'political_donation'
    __table_args__ = (
        sa.Index('employer_name_id', 'employer_name_id', 'employer_occupation_id'),
    )

    id = sa.Column(sa.Integer, primary_key=True)
    is_annonymous = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    contributor_id = sa.Column(sa.Integer, nullable=False, index=True)
    contributor_type_id = sa.Column(sa.Integer, nullable=False, index=True)
    contribution_type_id = sa.Column(sa.Integer, nullable=False, index=True)
    committee_id = sa.Column(sa.Integer, nullable=False, index=True)
    filing_period_id = sa.Column(sa.Integer, nullable=False, index=True)
    employer_name_id = sa.Column(sa.Integer, nullable=False)
    employer_occupation_id = sa.Column(sa.Integer, nullable=False)
    donation_date = sa.Column(sa.DateTime, nullable=False, index=True)
    donation_amount = sa.Column(sa.Numeric(10, 2), nullable=False, index=True)
    provided_name = sa.Column(sa.String(128), nullable=False)
    provided_address = sa.Column(sa.String(128), nullable=False)
    is_fixed_asset = sa.Column(sa.Integer, nullable=False)


class PoliticalDonationContributionType(Base):
    __tablename__ = 'political_donation_contribution_type'

    id = sa.Column(sa.Integer, primary_key=True)
    is_donation = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    type_name = sa.Column(sa.String(128), nullable=False, unique=True)
    type_name_short = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    type_slug = sa.Column(sa.String(32), nullable=False, index=True, server_default=sa.text("''"))
    type_description = sa.Column(sa.Text)


class PoliticalDonationEmployerName(Base):
    __tablename__ = 'political_donation_employer_name'

    id = sa.Column(sa.Integer, primary_key=True)
    employer_name = sa.Column(sa.String(128), nullable=False, unique=True)
    employer_slug = sa.Column(sa.String(32), nullable=False, index=True, server_default=sa.text("''"))
    employer_description = sa.Column(sa.Text)


class PoliticalDonationEmployerOccupation(Base):
    __tablename__ = 'political_donation_employer_occupation'

    id = sa.Column(sa.Integer, primary_key=True)
    occupation_name = sa.Column(sa.String(64), nullable=False, unique=True)
    occupation_slug = sa.Column(sa.String(32), nullable=False, index=True, server_default=sa.text("''"))
    occupation_description = sa.Column(sa.Text)


class PoliticalDonationFilingPeriod(Base):
    __tablename__ = 'political_donation_filing_period'

    id = sa.Column(sa.Integer, primary_key=True)
    period_name = sa.Column(sa.String(64), nullable=False, unique=True)
    period_slug = sa.Column(sa.String(32), nullable=False, index=True, server_default=sa.text("''"))
    period_description = sa.Column(sa.Text)


class Race(Base):
    __tablename__ = 'race'

    id = sa.Column(sa.Integer, primary_key=True)
    election_type = sa.Column(ENUM(u'primary', u'general'), nullable=False)
    election_year = sa.Column(YEAR(4), nullable=False)
    election_date = sa.Column(sa.Integer, nullable=False)
    seat_status = sa.Column(ENUM(u'filled', u'open seat', u'retired'), nullable=False)
    race_order = sa.Column(sa.Integer, nullable=False, index=True, server_default=sa.text("'0'"))
    race_name = sa.Column(sa.String(64), nullable=False, index=True)
    race_district = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    race_description = sa.Column(sa.Text)
    num_candidates = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    parties_short_text = sa.Column(sa.String(16), nullable=False, server_default=sa.text("''"))
    slug = sa.Column(sa.String(48), nullable=False)
    is_statewide = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    area = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))

    def __repr__(self):
        return '<Race election_type, election_year (%r %r)>' % (self.election_type,
                                               self.election_year)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RawDonation(Base):
    __tablename__ = 'raw_donations'

    id = sa.Column(sa.Integer, primary_key=True)
    FilerName = sa.Column(sa.String(128), nullable=False, index=True)
    Year = sa.Column(sa.String(32), nullable=False, index=True)
    Cycle = sa.Column(sa.String(32), nullable=False, index=True)
    DocType = sa.Column(sa.String(128), nullable=False, index=True)
    EntityName = sa.Column(sa.String(128), nullable=False)
    EntityAddressLine1 = sa.Column(sa.String(64), nullable=False)
    EntityAddressLine2 = sa.Column(sa.String(64), nullable=False)
    EntityCity = sa.Column(sa.String(64), nullable=False, index=True)
    EntityState = sa.Column(sa.String(32), nullable=False)
    EntityZip = sa.Column(sa.String(32), nullable=False)
    Occupation = sa.Column(sa.String(64), nullable=False)
    EmployerName = sa.Column(sa.String(128), nullable=False, index=True)
    EmployerAddressLine1 = sa.Column(sa.String(64), nullable=False)
    EmployerAddressLine2 = sa.Column(sa.String(64), nullable=False)
    EmployerCity = sa.Column(sa.String(64), nullable=False)
    EmployerState = sa.Column(sa.String(32), nullable=False)
    EmployerZip = sa.Column(sa.String(32), nullable=False)
    Date = sa.Column(sa.String(32), nullable=False)
    Amount = sa.Column(sa.String(32), nullable=False)
    Description = sa.Column(sa.String(255), nullable=False)
    Amended = sa.Column(sa.String(64), nullable=False, index=True)
    SubDate = sa.Column(sa.String(32), nullable=False)
    FiledBy = sa.Column(sa.String(128), nullable=False)


"""

class CiceroDistrict(Base):
    __tablename__ = 'cicero_district'

    id = sa.Column(sa.Integer, primary_key=True)
    cicero_id = sa.Column(sa.Integer, nullable=False)
    sk = sa.Column(sa.Integer, nullable=False)
    district_type = sa.Column(sa.String(64), nullable=False)
    valid_from = sa.Column(sa.String(32), nullable=False)
    valid_to = sa.Column(sa.String(32), nullable=False)
    country = sa.Column(sa.String(64), nullable=False)
    state = sa.Column(sa.String(8), nullable=False)
    city = sa.Column(sa.String(64), nullable=False)
    subtype = sa.Column(sa.String(64), nullable=False)
    district_id = sa.Column(sa.String(64), nullable=False)
    num_officials = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    label = sa.Column(sa.String(64), nullable=False)
    ocd_id = sa.Column(sa.String(128), nullable=False, server_default=sa.text("''"))
    data = sa.Column(sa.Text, nullable=False)
    last_update_date = sa.Column(sa.String(32), nullable=False)


class OpenAddressToDonorAddres(Base):
    __tablename__ = 'open_address_to_donor_address'

    open_address_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    donor_address_id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True)


class OpenAddress(Base):
    __tablename__ = 'open_addresses'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.String(16), nullable=False, index=True)
    street = sa.Column(sa.String(64), nullable=False, index=True)
    zipcode = sa.Column(sa.Integer, nullable=False, index=True)
    longitude = sa.Column(sa.Numeric(12, 8), nullable=False)
    latitude = sa.Column(sa.Numeric(12, 8), nullable=False)


class PoliticalDonationContributorAddressCiceroDetail(Base):
    __tablename__ = 'political_donation_contributor_address_cicero_details'

    id = sa.Column(sa.Integer, primary_key=True)
    address_id = sa.Column(sa.Integer, nullable=False)
    wkid = sa.Column(sa.Integer, nullable=False)
    score = sa.Column(sa.Integer, nullable=False)
    geo_x = sa.Column(sa.Numeric(12, 8), nullable=False)
    geo_y = sa.Column(sa.Numeric(12, 8), nullable=False)
    match_addr = sa.Column(sa.String(192), nullable=False)
    match_postal = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    match_country = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    locator = sa.Column(sa.String(64), nullable=False)
    match_region = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    match_subregion = sa.Column(sa.String(32), nullable=False, server_default=sa.text("''"))
    match_city = sa.Column(sa.String(64), nullable=False, server_default=sa.text("''"))
    partial_match = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    geoservice = sa.Column(sa.String(32), nullable=False)


class PoliticalDonationContributorAddressCiceroDistrictSet(Base):
    __tablename__ = 'political_donation_contributor_address_cicero_district_set'

    address_id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    cicero_district_id = sa.Column(sa.Integer, primary_key=True, nullable=False)


class PoliticalDonationContributorAddressCiceroRaw(Base):
    __tablename__ = 'political_donation_contributor_address_cicero_raw'

    id = sa.Column(sa.Integer, primary_key=True)
    address_id = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    addr1 = sa.Column(sa.String(128), nullable=False)
    zipcode5 = sa.Column(sa.Integer, nullable=False)
    district_ids = sa.Column(sa.String(128), nullable=False)
    geo_x = sa.Column(sa.Numeric(12, 8), nullable=False)
    geo_y = sa.Column(sa.Numeric(12, 8), nullable=False)
    match_addr = sa.Column(sa.String(192), nullable=False)
    raw_text = sa.Column(sa.Text, nullable=False)


t_political_donation_contributor_address_cicero_raw_ward = Table(
    'political_donation_contributor_address_cicero_raw_ward', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('contributor_address_id', sa.Integer, nullable=False, unique=True, server_default=sa.text("'0'")),
    sa.Column('geo_x', sa.String(16), nullable=False),
    sa.Column('geo_y', sa.String(16), nullable=False),
    sa.Column('ward', sa.Integer, nullable=False)
)

class SocialMediaAccount(Base):
    __tablename__ = 'social_media_accounts'

    id = sa.Column(sa.Integer, primary_key=True)
    social_media_site_id = sa.Column(sa.Integer, nullable=False)
    candidate_id = sa.Column(sa.Integer, nullable=False)
    account_url = sa.Column(sa.String(128), nullable=False)
    account_id = sa.Column(sa.String(64), nullable=False, server_default=sa.text("''"))
    account_name = sa.Column(sa.String(64), nullable=False, server_default=sa.text("''"))
    last_checked = sa.Column(sa.DateTime, nullable=False, index=True, server_default=sa.text("'1980-01-01 00:00:00'"))
    account_order = sa.Column(sa.Integer, nullable=False)


class SocialMediaSite(Base):
    __tablename__ = 'social_media_sites'

    id = sa.Column(sa.Integer, primary_key=True)
    social_name = sa.Column(sa.String(32), nullable=False)
    base_url = sa.Column(sa.String(64), nullable=False)


class SqlliteCampaign(Base):
    __tablename__ = 'sqllite_campaign'

    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer, nullable=False)
    cycle = sa.Column(sa.String(32), nullable=False)
    candidate_id = sa.Column(sa.Integer, nullable=False)
    position = sa.Column(sa.String(64), nullable=False)
    party = sa.Column(sa.String(64), nullable=False)


class SqlliteCandidate(Base):
    __tablename__ = 'sqllite_candidate'

    id = sa.Column(sa.Integer, primary_key=True)
    candidate_name = sa.Column(sa.String(128), nullable=False)


class SqlliteCandidateToCommittee(Base):
    __tablename__ = 'sqllite_candidate_to_committee'

    id = sa.Column(sa.Integer, primary_key=True)
    sqllite_candidate_id = sa.Column(sa.Integer, nullable=False)
    candidate_name = sa.Column(sa.String(128), nullable=False)
    committee_id = sa.Column(sa.Integer, nullable=False)
    committee_name = sa.Column(sa.String(128), nullable=False)



class UsContributionsByIndividualsActive(Base):
    __tablename__ = 'us_contributions_by_individuals_active'

    id = sa.Column(sa.Integer, primary_key=True)
    fec_committee_id = sa.Column(sa.String(9), nullable=False)
    amendment_indicator = sa.Column(sa.String(1), nullable=False)
    report_type = sa.Column(sa.String(3), nullable=False)
    primary_general = sa.Column(sa.String(5), nullable=False)
    image_number = sa.Column(sa.String(18), nullable=False)
    transaction_type = sa.Column(sa.String(3), nullable=False)
    entity_type = sa.Column(sa.String(3), nullable=False)
    contributor_name = sa.Column(sa.String(200), nullable=False)
    city = sa.Column(sa.String(30), nullable=False)
    state = sa.Column(sa.String(2), nullable=False)
    zipcode = sa.Column(sa.String(9), nullable=False)
    employer = sa.Column(sa.String(38), nullable=False)
    occupation = sa.Column(sa.String(38), nullable=False)
    transaction_date = sa.Column(Date, nullable=False)
    amount = sa.Column(sa.Numeric(14, 2), nullable=False)
    from_fec_id = sa.Column(sa.String(9), nullable=False)
    transaction_id = sa.Column(sa.String(32), nullable=False)
    file_num = sa.Column(Bigsa.Integer, nullable=False)
    memo_code = sa.Column(sa.String(1), nullable=False)
    memo_text = sa.Column(sa.String(100), nullable=False)
    fec_record_number = sa.Column(Bigsa.Integer, nullable=False)

"""
