package YuzhouLiA1P4;

public class Tree extends Graph {
	int totalWeight;

	public Tree(int N) {
		super(N);
		super.numE = N - 1;
	}

	public int calculateWeight() {
		int result = 0;
		for(int i=0;i<super.numN;i++) {
			for(int j=0;j<super.adList.get(i).size();j++) {
				if (i<adList.get(i).get(j).v) {
					result+= super.adList.get(i).get(j).weight;
				}
			}
		}
		this.totalWeight = result;
		return result;
	}

}
