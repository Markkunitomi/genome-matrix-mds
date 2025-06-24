'''
Created on Jun 2, 2017

@author: markkunitomi
'''

import sys
import csv
import numpy as np
import sklearn
from sklearn.cluster import DBSCAN
from sklearn import metrics

def Run_DBSCAN	(
					Data,
					Labels_true,
					Epsilon,
					Min_group,
				):

	##################
	### Run DBSCAN ###
	##################

	db = DBSCAN(eps=float(Epsilon), min_samples= int(Min_group), metric='precomputed').fit(Data)

	############################################
	### Parse Results from DBscan and Report ###
	############################################

	labels = db.labels_
	n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
	n_outliers_ = np.count_nonzero(labels == -1)

	##################################
	### Get position of each label ###
	##################################

	position_to_cluster_dict={}
	for index, s in enumerate(labels):
		position_to_cluster_dict[index] = s

	##################################
	### Get position of each Class ###
	##################################

	position_to_class_dict={}
	for index, s in enumerate(Labels_true):
		position_to_class_dict[index] = s

	#########################################
	### Get Cluster members of each Class ###
	#########################################

	Class_cluster_members_dict={}
	for Class in set(Labels_true):
		members=[]
		for index, s in enumerate(Labels_true):
			if Class == s:
				members.append(position_to_cluster_dict[index])
		Class_cluster_members_dict[Class] = members

	#########################################
	### Get Class members of each Cluster ###
	#########################################

	Cluster_class_members_dict={}
	for Cluster in set(labels):
		members=[]
		for index, s in enumerate(labels):
			if Cluster == s:
				members.append(position_to_class_dict[index])
		Cluster_class_members_dict[Cluster] = members

	################################
	### Return results per Class ###
	################################

	All_Class_metadata=[]
	Class_scores_all=[]

	for Class in Class_cluster_members_dict:

		##################################
		### Return General Class Stats ###
		##################################

		Class_metadata=[Epsilon, Min_group]
		Cluster_scores=[]
		Class_all_cluster_metadata=[]

		all_members				=	Class_cluster_members_dict[Class]
		set_members				=	set(all_members)
		num_members				=	len(all_members)
		num_outliers			=	all_members.count(-1)
		num_clustered_members	=	num_members - num_outliers
		clusters				=	set(list(filter(lambda a: a != -1, all_members)))
		num_clusters			=	len(clusters)

		##############################################################################################################
		### For each cluster in the class, find how many members, which classes they are from, and calculate score ###
		##############################################################################################################

		for Member in set_members:
			if Member != -1:																			# Outliers aren't clusters

				Individual_cluster_metadata=[]
				Individual_cluster_members_metadata=[]

				Cluster_members_count = len(Cluster_class_members_dict[Member])

				for item in set(Cluster_class_members_dict[Member]):

					### Return classes in cluster and count ###
					Cluster_member_metadata=[]
					Cluster_member_metadata.append(item)												# Class in cluster
					Class_count = Cluster_class_members_dict[Member].count(item)
					Cluster_member_metadata.append(Class_count)											# Number of class in cluster
					Individual_cluster_members_metadata.append(Cluster_member_metadata)

					### Calculate Cluster score ###
					if item == Class:
						Cluster_score = (Class_count**2 / Cluster_members_count)						# Cluster score is weighted by number of members, i.e. = the proportion of the cluster from a given class * the number of class members in the cluster

				############################
				### Return cluster score ###
				############################

				Cluster_scores.append(Cluster_score)

				################################
				### Return per cluster stats ###
				################################

				Individual_cluster_metadata.append(Member)												# Cluster name
				Individual_cluster_metadata.append(Cluster_members_count)								# Number of members
				Individual_cluster_metadata.append(Cluster_score)										# Cluster score
				Individual_cluster_metadata.append(Individual_cluster_members_metadata)					# Names and number of each class in cluster
				Class_all_cluster_metadata.append(Individual_cluster_metadata)							# Add Cluster entry

		#############################
		### Calculate Class Score ###
		#############################

		Class_score =  (sum(Cluster_scores) / num_members)												# Class score is the weighted (by number of members) average of the cluster scores
		Class_scores_all.append(Class_score)

		##################################
		### Return General Class Stats ###
		##################################

		Class_metadata.append(Class)
		Class_metadata.append(num_members)
		Class_metadata.append(num_clustered_members)
		Class_metadata.append(num_outliers)
		Class_metadata.append(num_clusters)
		Class_metadata.append(Class_score)
		Class_metadata.append(Class_all_cluster_metadata)

		All_Class_metadata.append(Class_metadata)

	Run_score = (sum(Class_scores_all)/ len(Class_scores_all))											# The run score is the un-weighted average of the class scores

	####################################
	### Get Global Clustering Scores ###
	####################################

	Homogeneity_score			=	metrics.homogeneity_score(Labels_true, labels)
	Completeness_score			=	metrics.completeness_score(Labels_true, labels)

	return	[
				Min_group,
				Epsilon,
				n_clusters_,
				n_outliers_,
				Run_score,
				Homogeneity_score,
				Completeness_score
			], All_Class_metadata

def Run_Multi_DBSCAN(
							Labels,
							Distance_matrix,
							Metadata_file,
							Run_parameters,
							Basic_parameters
						):

	Epsilon_low				=		Run_parameters.Epsilon_low
	Epsilon_high			=		Run_parameters.Epsilon_high
	Epsilon_increment		=		Run_parameters.Epsilon_increment
	Min_group_low			=		Run_parameters.Min_group_low
	Min_group_high			=		Run_parameters.Min_group_high
	Min_group_increment		=		Run_parameters.Min_group_increment
	Out_path				=		Basic_parameters.Out_path

	#####################################
	### Get Metadata_file for ground truth ###
	#####################################

	if Metadata_file == None:
		with open("%s/Genome_metadata.tsv" %Out_path, 'r') as file:
			Metadata = [line.rstrip() for line in file.readlines()]
	else:
		with open(Metadata_file, 'r') as file:
			Metadata = [line.rstrip() for line in file.readlines()]

	####################################################
	### Pull genus and species for each genome Label ###
	####################################################

	Species_dict={}
	Genus_dict={}
	Family_dict={}

	for Line in Metadata[1:]:
		Line = Line.split("\t")
		Species_dict[Line[0]] = Line[2]
		Genus_dict[Line[0]] = Line[3]
		Family_dict[Line[0]] = Line[4]

	Species_Labels=[]
	Genus_Labels=[]
	Family_Labels=[]

	for Name in Labels:
		Species_Labels.append(Species_dict[Name])
		Genus_Labels.append(Genus_dict[Name])
		Family_Labels.append(Family_dict[Name])

	###############################################################################################
	### Make numpy arrays for comparing DBSCAN labels to ground truth at genus or species level ###
	###############################################################################################

	Species_labels_true = np.array(Species_Labels)
	Genus_labels_true = np.array(Genus_Labels)
	Family_labels_true = np.array(Family_Labels)

	###########################################################
	### Make numpy array from distance matrix to run DBSCAN ###
	###########################################################

	Data = np.array(Distance_matrix)

	############################################################
	### Column labels for global scores from DBSCAN analysis ###
	############################################################

	General_stats =	[[
						'Min_group',
						'Epsilon',
						'n_clusters_',
						'n_outliers_',
						'Run_score',
						'Homogeneity_score',
						'Completeness_score',
						'V_measure',
						'Adjusted_rand_score',
						'Adjusted_mutual_info_score'
					]]

	###########################################################
	### Column labels for class scores from DBSCAN analysis ###
	###########################################################

	Class_stats = 		[[	'Kmer_size',
							'Sketch_size',
							'Epsilon',
							'Min_group',
							"Class",
							"Num_members",
							"Num_clustered_members",
							"Num_outlier_members",
							"Num_clusters",
							"Class_score",
							"Clusters"
						]]

	#####################################################################
	### Run loop of DBSCAN for all EPS and Min_group parameter values ###
	#####################################################################

	def DBSCAN_parameter_scan(Labels_true, Class_labels, Prefix):

		Temp_General_stats=General_stats[:]
		Temp_Class_stats=Class_stats[:]

		for x in range(int(Min_group_low), int(Min_group_high)+int(Min_group_increment), int(Min_group_increment)):
			for y in range(int(float(Epsilon_low) * 1000), int(float(Epsilon_high) * 1000) + int(float(Epsilon_increment) * 1000), int(float(Epsilon_increment) * 1000)):

				Stat, Class_metadata = Run_DBSCAN(		Labels,
														Data,
														y * 0.001,
														x,
														Metadata,
														Labels_true,
														Run_parameters,
														Basic_parameters
													)

				Temp_General_stats.append(Stat)
				Temp_Class_stats.append(Class_metadata)

		###################################
		### Write results as .tsv files ###
		###################################

		with open("%s/%s_DBSCAN.tsv" %(Out_path, Prefix), 'w') as file:
			writer = csv.writer(file, delimiter="\t")
			for line in Temp_General_stats:
				writer.writerow(line)

		with open("%s/%s_report.tsv" %(Out_path, Prefix), 'w') as file:
			writer = csv.writer(file, delimiter="\t")
			writer.writerow(Temp_Class_stats[0])
			for Classifier in set(Class_labels):
				for List1 in Temp_Class_stats[1:]:
					for item in List1:
						if item[4] == Classifier:
							writer.writerow(item)
		return Temp_General_stats

	##################################################################################
	### Run DBSCAN_parameter_scan scoring at Species, Genus, and Family as Classes ###
	##################################################################################

	Species_Stats = DBSCAN_parameter_scan(Species_labels_true, Species_Labels, "Species")
	Genus_Stats = DBSCAN_parameter_scan(Genus_labels_true, Genus_Labels, "Genus")
	Family_Stats = DBSCAN_parameter_scan(Family_labels_true, Family_Labels, "Family")

	########################################################################################################################
	### Find number of different species/genus and use to find runs of DBSCAN that produced most similar cluster numbers ###
	########################################################################################################################

	EPS = []
	for STAT in Species_Stats[1:]:
		EPS.append(STAT[4])

	Best_species_cluster = min(EPS, key=lambda x:abs(x-len(set(Species_Labels))))

	Best_genus_cluster = min(EPS, key=lambda x:abs(x-len(set(Genus_Labels))))

	Best_family_cluster = min(EPS, key=lambda x:abs(x-len(set(Family_Labels))))

	Best_species_Combos=[]
	Best_genus_Combos=[]
	Best_family_Combos=[]

	for STAT in Species_Stats[1:]:
		if STAT[4] == Best_species_cluster:
			Best_species_Combos.append([STAT[2], STAT[3]])
		if STAT[4] == Best_genus_cluster:
			Best_genus_Combos.append([STAT[2], STAT[3]])
		if STAT[4] == Best_family_cluster:
			Best_family_Combos.append([STAT[2], STAT[3]])

	####################
	### Print Report ###
	####################

	print("\t###   INPUT   ###")
	print("\n\tEpsilon range:\t\t\t%0.3f-%0.3f" %(float(Epsilon_low), float(Epsilon_high)))
	print("\tEpsilon change increment:\t%0.3f" %float(Epsilon_increment))
	print("\tMin Group range:\t\t%s-%s" %(Min_group_low, Min_group_high))
	print("\tMin Group change increment:\t%s" %Min_group_increment)
	print("\tNumber of Species:\t\t%d" % len(set(Species_Labels)))
	print("\tNumber of Genuses:\t\t%d" % len(set(Genus_Labels)))
	print("\tNumber of Families:\t\t%d" % len(set(Family_Labels)))

	print("\n\t###    RESULTS    ###")
	print("\n\tNumber of Species Clusters:\t%d (%0.1f%%)" %(Best_species_cluster, float(Best_species_cluster/len(set(Species_Labels))*100)))
	print("\tBest Min_group / EPS Combos (species):\t\t\tMin_Group\tEPS")

	for Combo in Best_species_Combos:
		print("\t\t\t\t\t\t\t\t\t%i\t%0.3f" %(Combo[0],Combo[1]))

	print("\n\tNumber of Genus Clusters:\t%d (%0.1f%%)" %(Best_genus_cluster, float(Best_genus_cluster/len(set(Genus_Labels))*100)))
	print("\tBest Min_group / EPS Combos (genus):\t\t\tMin_Group\tEPS")

	for Combo in Best_genus_Combos:
		print("\t\t\t\t\t\t\t\t\t%i\t%0.3f" %(Combo[0],Combo[1]))

	print("\n\tNumber of Family Clusters:\t%d (%0.1f%%)" %(Best_family_cluster, float(Best_family_cluster/len(set(Family_Labels))*100)))
	print("\tBest Min_group / EPS Combos (family):\t\t\tMin_Group\tEPS")

	for Combo in Best_family_Combos:
		print("\t\t\t\t\t\t\t\t\t%i\t%0.3f" %(Combo[0],Combo[1]))

###########################
###		Unit Test		###
###########################

# if __name__ == "__main__":
#
#
# 	sys.exit(	DBSCAN_parameter_scan(
# 										Run_Multi_DBSCAN(
# 										Labels,
# 										Distance_matrix,
# 										Metadata_file,
# 										Run_parameters,
# 										Basic_parameters
# 									)
# 			)
