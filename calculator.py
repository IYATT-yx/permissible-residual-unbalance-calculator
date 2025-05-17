import math

class Calculator:
    @staticmethod
    def calcPermissibleResidualUnbalance(rotorMass: float, speed: float, qualityGrades: float, correctionRadius: float = None) -> float:
        """计算许用剩余不平衡量

        Args:
            rotorMass (float): 转子质量 kg
            speed (float): 转速 r/min
            qualityGrades (float): 品质等级
            correctionRadius (float, optional): 校正半径 mm.

        Returns:
            float: 许用剩余不平衡量。如果提供了校正半径，结果为 g；否则为 g·mm。
        """
        permissibleResidualUnbalance = 3 * qualityGrades * rotorMass * 10**4 / (math.pi * speed)
        if correctionRadius is None:
            return permissibleResidualUnbalance
        else:
            return permissibleResidualUnbalance / correctionRadius
        
    @staticmethod
    def calcSpeed(rotorMass: float, qualityGrades: float, permissibleResidualUnbalance: float, unit: str = 'gmm', correctionRadius: float = None) -> float:
        """计算转速

        Args:
            rotorMass (float): 转子质量 kg
            qualityGrades (float): 品质等级
            permissibleResidualUnbalance (float): 许用剩余不平衡量。
            unit (str): 许用剩余不平衡量的单位。gmm 或 g
            correctionRadius (float, optional): 校正半径 mm。如果 unit 值为 g，则必须提供校正半径。

        Returns:
            float: 转速 r/min
        """
        if unit == 'g':
            permissibleResidualUnbalance *= correctionRadius

        return 3 * qualityGrades * rotorMass * 10**4 / (math.pi * permissibleResidualUnbalance)
    
    @staticmethod
    def calcQualityGrades(rotorMass: float, speed: float, permissibleResidualUnbalance: float, unit: str = 'gmm', correctionRadius: float = None) -> float:
        """计算品质等级

        Args:
            rotorMass (float): 转子质量 kg
            speed (float): 转速 r/min
            permissibleResidualUnbalance (float): 许用剩余不平衡量。
            unit (str): 许用剩余不平衡量的单位。gmm 或 g
            correctionRadius (float, optional): 校正半径 mm。如果 unit 值为 g，则必须提供校正半径。

        Returns:
            float: 品质等级
        """
        if unit == 'g':
            permissibleResidualUnbalance *= correctionRadius

        return permissibleResidualUnbalance * math.pi * speed / (3 * rotorMass * 10**4)

