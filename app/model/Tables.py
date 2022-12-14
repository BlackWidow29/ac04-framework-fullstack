
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, Float, Boolean, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ac04.sqlite', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'tbl_cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(20), nullable=False)
    agencia = Column(BigInteger, nullable=False)
    conta = Column(BigInteger, nullable=False)
    email = Column(String(100), nullable=False)

    def __init__(self, nome, sobrenome, agencia, conta, email):
        self.nome= nome
        self.sobrenome=sobrenome
        self.agencia=agencia
        self.conta=conta
        self.email=email

    def __repr__(self):
        return "<Cliente: {}>".format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Uf(Base):
    __tablename__ = 'tbl_uf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uf = Column(String(2), nullable=False)

    def __repr__(self):
        return "<Uf: {}>".format(self.uf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Endereco(Base):
    __tablename__ = 'tbl_endereco'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cep = Column(String(9), nullable=False)
    bairro = Column(String(100), nullable=False)
    numero = Column(Integer, nullable=False)
    cidade = Column(String(100), nullable=False)
    id_estado = Column(Integer, ForeignKey('tbl_uf.id'))
    estado = relationship("Uf")
    complemento = Column(String(100), nullable=True)
    id_cliente = Column(Integer, ForeignKey('tbl_cliente.id'))
    cliente = relationship("Cliente")

    def __repr__(self):
        return "<Endereco: {}>".format(self.cep)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Telefone(Base):
    __tablename__ = 'tbl_telefone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(14), nullable=False)
    principal = Column(Boolean, nullable=False)
    id_cliente = Column(Integer, ForeignKey('tbl_cliente.id'))
    cliente = relationship("Cliente")

    def __repr__(self):
        return "<Uf: {}>".format(self.uf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Contrato(Base):
    __tablename__ = 'tbl_contrato'
    numero_contrato = Column(Integer, primary_key=True, autoincrement=True)
    saldo_devedor = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    taxa = Column(Float, nullable=False)
    situacao_contrato = Column(Integer, nullable=False)
    quantidade_parcelas = Column(Integer, nullable=False)
    data_contratacao = Column(Date, nullable=False)
    cliente_id = Column(Integer, ForeignKey('tbl_cliente.id'))
    cliente = relationship("Cliente")

    def __repr__(self):
        return "<Contrato: {}>".format(self.uf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Parcelas(Base):
    __tablename__ = 'tbl_parcelas'
    numero_parcela = Column(Integer, primary_key=True, autoincrement=True)
    valor_parcela = Column(Float, nullable=False)
    situacao_parcela = Column(Integer, nullable=False)
    contrato_id = Column(Integer, ForeignKey('tbl_contrato.numero_contrato'))
    contrato = relationship("Contrato")

    def __repr__(self):
        return "<Parcela: {}>".format(self.uf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
