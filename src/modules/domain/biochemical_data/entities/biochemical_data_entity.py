from dataclasses import dataclass

from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class BiochemicalData(BaseEntity):
    total_proteins: Float(2) = Column(Float(2), nullable=True)
    albumin: Float(2) = Column(Float(2), nullable=True)
    urea: Float(2) = Column(Float(2), nullable=True)
    uric_acid: Float(2) = Column(Float(2), nullable=True)
    creatinine: Float(2) = Column(Float(2), nullable=True)
    total_cholesterol: Float(2) = Column(Float(2), nullable=True)
    hdl: Float(2) = Column(Float(2), nullable=True)
    ldl: Float(2) = Column(Float(2), nullable=True)
    glycemia: Float(2) = Column(Float(2), nullable=True)
    hda1c: Float(2) = Column(Float(2), nullable=True)
    fasting_glycemia: Float(2) = Column(Float(2), nullable=True)
    post_prandial_glycemia: Float(2) = Column(Float(2), nullable=True)
    total_bilirubin: Float(2) = Column(Float(2), nullable=True)
    biliburin_direct: Float(2) = Column(Float(2), nullable=True)
    alkaline_phosphatase: Float(2) = Column(Float(2), nullable=True)
    ast_tgo: Float(2) = Column(Float(2), nullable=True)
    alt_tgp: Float(2) = Column(Float(2), nullable=True)
    ygt: Float(2) = Column(Float(2), nullable=True)

    appointment_id: UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("appointment.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    appointment = relationship("Appointment", back_populates="biochemical_data")

    def __init__(
        self,
        total_proteins: Float(2) = None,
        albumin: Float(2) = None,
        urea: Float(2) = None,
        uric_acid: Float(2) = None,
        creatinine: Float(2) = None,
        total_cholesterol: Float(2) = None,
        hdl: Float(2) = None,
        ldl: Float(2) = None,
        glycemia: Float(2) = None,
        hda1c: Float(2) = None,
        fasting_glycemia: Float(2) = None,
        post_prandial_glycemia: Float(2) = None,
        total_bilirubin: Float(2) = None,
        biliburin_direct: Float(2) = None,
        alkaline_phosphatase: Float(2) = None,
        ast_tgo: Float(2) = None,
        alt_tgp: Float(2) = None,
        ygt: Float(2) = None,
        appointment_id: UUID = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.total_proteins = total_proteins
        self.albumin = albumin
        self.urea = urea
        self.uric_acid = uric_acid
        self.creatinine = creatinine
        self.total_cholesterol = total_cholesterol
        self.hdl = hdl
        self.ldl = ldl
        self.glycemia = glycemia
        self.hda1c = hda1c
        self.fasting_glycemia = fasting_glycemia
        self.post_prandial_glycemia = post_prandial_glycemia
        self.total_bilirubin = total_bilirubin
        self.biliburin_direct = biliburin_direct
        self.alkaline_phosphatase = alkaline_phosphatase
        self.ast_tgo = ast_tgo
        self.alt_tgp = alt_tgp
        self.ygt = ygt
        self.appointment_id = appointment_id
